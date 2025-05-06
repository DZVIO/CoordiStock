import json
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import django
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.views.decorators.cache import never_cache
import os
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from rest_framework import generics, filters
from django.db.models import Q
from app.models import Movimiento, Activo, Agente, Terminal, Area, Detalle_movimiento, Operador
from .serializers import TerminalSerializer, ActivoSerializer, AgenteSerializer, AreaSerializer
from app.forms import MovimientoForm, DetalleMovimientoForm

@method_decorator(never_cache, name='dispatch')
def lista_movimiento(request):
    nombre = {
        'titulo': 'Listado de movimientos',
        'movimientos': Movimiento.objects.all()
    }
    return render(request, 'movimiento/listar.html',nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'movimiento/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        movimientos = Movimiento.objects.all()
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de movimientos'
        context['entidad'] = 'Listado de movimientos'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['crear_url'] = reverse_lazy('app:movimiento_crear')
        context['movimientos_con_detalles'] = [
            {'movimiento': movimiento, 
            'detalle_movimiento': Detalle_movimiento.objects.filter(id_movimiento=movimiento)
            }
            for movimiento in movimientos
        ]
        return context

###### API'S ######
class TerminalAPI(generics.ListAPIView):
    queryset = Terminal.objects.filter(Q(estado=True))
    serializer_class = TerminalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['terminal', 'nombre', 'direccion'] 

class ActivoAPI(generics.ListAPIView):
    serializer_class = ActivoSerializer
    filter_backends = []
    search_fields = ['id_marca__marca', 'activo', 'modelo', 'n_serie', 'renting', 'disponibilidad']

    def get_queryset(self):
        queryset = Activo.objects.filter(estado=True)

        tipo = self.request.GET.get('tipo')
        categoria = self.request.GET.get('categoria')
        tipo_mov = self.request.GET.get('tipo_mov') 

        if tipo in ['True', 'False']:
            queryset = queryset.filter(tipo=(tipo == 'True'))

        if categoria:
            queryset = queryset.filter(categoria=categoria)

        if tipo_mov in ['Asignación', 'Préstamo', 'Disposición final']: 
            queryset = queryset.filter(disponibilidad=True, mantenimiento=False)

        elif tipo_mov == 'Devolución':
            queryset = queryset.filter(disponibilidad=False)

        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        search_query = self.request.GET.get('search')
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(id_marca__marca__icontains=search_query) |
                Q(activo__icontains=search_query) |
                Q(modelo__icontains=search_query) |
                Q(n_serie__icontains=search_query)
            )
        return queryset
    
class AgenteAPI(generics.ListAPIView):
    serializer_class = AgenteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'codigo', 'email', 'id_area__area', 'id_terminal__terminal']

    def get_queryset(self):
        queryset = Agente.objects.filter(estado=True)
        activo_id = self.request.query_params.get('activo', None)

        if activo_id:
            try:
                activo = Activo.objects.get(pk=activo_id)
                if activo.renting:
                    queryset = queryset.filter(id_area__area__in=['T.I', 'Call Center'])
            except Activo.DoesNotExist:
                pass 

        return queryset

class AreaAPI(generics.ListAPIView):
    queryset = Area.objects.filter(estado=True)
    serializer_class = AreaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['area']

###### CREAR ######
@method_decorator(never_cache, name='dispatch')
class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'movimiento/crear.html'
    success_url = reverse_lazy('app:movimiento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar movimiento'
        context['entidad'] = 'Registrar movimiento'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['detallemovimiento_form'] = DetalleMovimientoForm()
        return context

    def form_valid(self, form):
        try:
            movimiento = form.save(commit=False)
            user = self.request.user

            try:
                operador = Operador.objects.get(user=user)
                movimiento.responsable_content_type = ContentType.objects.get_for_model(Operador)
                movimiento.responsable_object_id = operador.id
            except Operador.DoesNotExist:
                movimiento.responsable_content_type = ContentType.objects.get_for_model(user)
                movimiento.responsable_object_id = user.id

            detalle_movimiento_json = self.request.POST.get('detalle_movimiento')
            tipo_mantenimiento = self.request.POST.get('tipo_mantenimiento')

            if detalle_movimiento_json:
                try:
                    detalle_movimiento = json.loads(detalle_movimiento_json)
                except json.JSONDecodeError:
                    detalle_movimiento = []
            else:
                detalle_movimiento = []

            movimiento.save()

            for detalle in detalle_movimiento:
                try:
                    id_activo = detalle.get('idactivo')
                    motivo = detalle.get('motivo')
                    id_agente = detalle.get('idagente')
                    nomenclatura = detalle.get('nomenclature')
                    id_area = detalle.get('idarea')
                    observaciones = detalle.get('observaciones')

                    activo = Activo.objects.get(pk=id_activo)

                    if movimiento.tipo_mov == Movimiento.t_m.ASIGNACION:
                        activo.disponibilidad = False
                        activo.save()

                    if movimiento.tipo_mov == Movimiento.t_m.PRESTAMO:
                        activo.disponibilidad = False
                        activo.save()

                    if movimiento.tipo_mov == Movimiento.t_m.DEVOLUCION:
                        activo.disponibilidad = True
                        activo.save()

                    if movimiento.tipo_mov == Movimiento.t_m.D_FINAL:
                        activo.estado = False
                        activo.save()

                    if movimiento.tipo_mov == Movimiento.t_m.MANTENIMIENTO:
                        if tipo_mantenimiento == 'Recepción':
                            activo.mantenimiento = True
                        elif tipo_mantenimiento == 'Entrega':
                            activo.mantenimiento = False
                        activo.save()

                    Detalle_movimiento.objects.create(
                        id_movimiento=movimiento,
                        id_activo=activo,
                        motivo=motivo,
                        id_agente=Agente.objects.get(pk=id_agente),
                        nomenclatura=nomenclatura,
                        id_area=Area.objects.get(pk=id_area),
                        observaciones=observaciones
                    )

                except Exception as detalle_error:
                    print(f"Error creando detalle de movimiento: {detalle_error}")

            success_url = reverse_lazy('app:movimiento_lista')
            return redirect(success_url)

        except Exception as e:
            print(f"Error general: {e}")
            return JsonResponse({'success': False, 'message': f'Error general: {str(e)}'})
###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoUpdateView(UpdateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'movimiento/crear.html'
    success_url = reverse_lazy('app:movimiento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar movimiento'
        context['entidad'] = 'Editar movimiento'
        context['error'] = 'Este movimiento ya existe'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        return context

    def form_valid(self, form):
        movimiento = form.cleaned_data.get('movimiento').lower()
        response = super().form_valid(form)
        success_url = reverse('app:movimiento_lista') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class MovimientoDeleteView(DeleteView):
    model = Movimiento
    template_name = 'movimiento/eliminar.html'
    success_url = reverse_lazy('app:movimiento_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar movimiento'
        context['entidad'] = 'Eliminar movimiento'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'movimiento eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el movimiento.'})