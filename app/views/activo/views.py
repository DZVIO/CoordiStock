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
from app.models import Activo, Movimiento, Detalle_movimiento
from app.forms import ActivoForm

@method_decorator(never_cache, name='dispatch')
def lista_activo(request):
    nombre = {
        'titulo': 'Listado de activos',
        'activos': Activo.objects.all()
    }
    return render(request, 'activo/listar.html', nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class ActivoListView(ListView):
    model = Activo
    template_name = 'activo/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de activos'
        context['entidad'] = 'Listado de activos'
        context['listar_url'] = reverse_lazy('app:activo_lista')
        context['crear_url'] = reverse_lazy('app:activo_crear')
        context['detalles_movimiento'] = Detalle_movimiento.objects.select_related('id_movimiento', 'id_activo', 'id_area', 'id_agente').all()
        return context

###### CREAR ######
@method_decorator(never_cache, name='dispatch')
class ActivoCreateView(CreateView):
    model = Activo
    form_class = ActivoForm
    template_name = 'activo/crear.html'
    success_url = reverse_lazy('app:activo_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar activo'
        context['entidad'] = 'Registrar activo'
        context['listar_url'] = reverse_lazy('app:activo_lista')
        return context
    
###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class ActivoUpdateView(UpdateView):
    model = Activo
    form_class = ActivoForm
    template_name = 'activo/crear.html'
    success_url = reverse_lazy('app:activo_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar activo'
        context['entidad'] = 'Editar activo'
        context['error'] = 'Este activo ya existe'
        context['listar_url'] = reverse_lazy('app:activo_lista')
        return context

    def form_valid(self, form):
        
        activo = form.cleaned_data.get('activo')
        response = super().form_valid(form)
        success_url = reverse('app:activo_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class ActivoDeleteView(DeleteView):
    model = Activo
    template_name = 'activo/eliminar.html'
    success_url = reverse_lazy('app:activo_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar activo'
        context['entidad'] = 'Eliminar activo'
        context['listar_url'] = reverse_lazy('app:activo_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Activo eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el activo.'})
