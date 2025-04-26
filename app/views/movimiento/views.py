import json
from django.contrib import messages
import django
from django.contrib.auth.decorators import login_required
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
from app.models import Movimiento, Activo, Agente, Terminal, Area, Detalle_movimiento
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
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de movimientos'
        context['entidad'] = 'Listado de movimientos'
        context['listar_url'] = reverse_lazy('app:movimiento_lista')
        context['crear_url'] = reverse_lazy('app:movimiento_crear')
        return context

###### API'S ######
class TerminalAPI(generics.ListAPIView):
    queryset = Terminal.objects.filter(Q(estado=True))
    serializer_class = TerminalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['terminal', 'nombre', 'direccion'] 

class ActivoAPI(generics.ListAPIView):
    serializer_class = ActivoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id_marca__marca', 'activo', 'modelo', 'n_serie']

    def get_queryset(self):
        queryset = Activo.objects.filter(estado=True, disponibilidad=True)

        tipo = self.request.GET.get('tipo')
        categoria = self.request.GET.get('categoria')

        if tipo in ['True', 'False']:
            queryset = queryset.filter(tipo=(tipo == 'True'))

        if categoria:
            queryset = queryset.filter(categoria=categoria)

        return queryset
    
class AgenteAPI(generics.ListAPIView):
    queryset = Agente.objects.filter(estado=True)
    serializer_class = AgenteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'codigo', 'email', 'id_area__area', 'id_terminal__terminal']

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
            detalle_movimiento_json = self.request.POST.get('detalle_movimiento')

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

                    Detalle_movimiento.objects.create(
                        id_movimiento=movimiento,
                        id_activo=Activo.objects.get(pk=id_activo),
                        motivo=motivo,
                        id_agente=Agente.objects.get(pk=id_agente),
                        nomenclatura=nomenclatura,
                        id_area=Area.objects.get(pk=id_area),
                        observaciones=observaciones
                    )
                except Exception as detalle_error:
                    print(f"Error creando detalle de movimiento: {detalle_error}")
            
            return JsonResponse({'success': True, 'message': 'Movimiento creado con éxito.'})
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