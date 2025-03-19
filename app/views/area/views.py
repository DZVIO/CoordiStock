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
from app.models import Area
from app.forms import AreaForm

@method_decorator(never_cache, name='dispatch')
def lista_area(request):
    nombre = {
        'titulo': 'Listado de areas',
        'areas': Area.objects.all()
    }
    return render(request, 'area/listar.html',nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class AreaListView(ListView):
    model = Area
    template_name = 'area/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de areas'
        context['entidad'] = 'Listado de areas'
        context['listar_url'] = reverse_lazy('app:area_lista')
        context['crear_url'] = reverse_lazy('app:area_crear')
        return context

###### CREAR ######
@method_decorator(never_cache, name='dispatch')
class AreaCreateView(CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/crear.html'
    success_url = reverse_lazy('app:area_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar area'
        context['entidad'] = 'Registrar area'
        context['listar_url'] = reverse_lazy('app:area_lista')
        return context
    
    def form_valid(self, form):
        area = form.cleaned_data.get('area').lower()
        
        if Area.objects.filter(area__iexact=area).exists():
            form.add_error('area', 'Ya existe una area registrada con ese nombre.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        success_url = reverse('app:area_crear') + '?created=True'
        return redirect(success_url)

###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/crear.html'
    success_url = reverse_lazy('app:area_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar area'
        context['entidad'] = 'Editar area'
        context['error'] = 'Esta area ya existe'
        context['listar_url'] = reverse_lazy('app:area_lista')
        return context

    def form_valid(self, form):
        area = form.cleaned_data.get('area').lower()
        response = super().form_valid(form)
        success_url = reverse('app:area_lista') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class AreaDeleteView(DeleteView):
    model = Area
    template_name = 'area/eliminar.html'
    success_url = reverse_lazy('app:area_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar area'
        context['entidad'] = 'Eliminar area'
        context['listar_url'] = reverse_lazy('app:area_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'area eliminada con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar la area.'})