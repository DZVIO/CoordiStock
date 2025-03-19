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
from app.models import Agente
from app.forms import AgenteForm

@method_decorator(never_cache, name='dispatch')
def lista_agente(request):
    nombre = {
        'titulo': 'Listado de agentes',
        'agentes': Agente.objects.all()
    }
    return render(request, 'agente/listar.html',nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class AgenteListView(ListView):
    model = Agente
    template_name = 'agente/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de agentes'
        context['entidad'] = 'Listado de agentes'
        context['listar_url'] = reverse_lazy('app:agente_lista')
        context['crear_url'] = reverse_lazy('app:agente_crear')
        return context

###### CREAR ######
@method_decorator(never_cache, name='dispatch')
class AgenteCreateView(CreateView):
    model = Agente
    form_class = AgenteForm
    template_name = 'agente/crear.html'
    success_url = reverse_lazy('app:agente_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar agente'
        context['entidad'] = 'Registrar agente'
        context['listar_url'] = reverse_lazy('app:agente_lista')
        return context
    
    def form_valid(self, form):
        numero_documento = form.cleaned_data.get('numero_documento')
        codigo= form.cleaned_data.get('codigo')

        if Agente.objects.filter(numero_documento=numero_documento).exists():
            form.add_error('numero_documento', 'Ya existe un agente registrado con este número de documento.')
            return self.form_invalid(form)
        
        if Agente.objects.filter(codigo=codigo).exists():
            form.add_error('codigo', 'Ya existe un agente registrado con este codigo.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        success_url = reverse('app:agente_crear') + '?created=True'
        return redirect(success_url)

###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class AgenteUpdateView(UpdateView):
    model = Agente
    form_class = AgenteForm
    template_name = 'agente/crear.html'
    success_url = reverse_lazy('app:agente_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar agente'
        context['entidad'] = 'Editar agente'
        context['error'] = 'Este agente ya existe'
        context['listar_url'] = reverse_lazy('app:agente_lista')
        return context

    def form_valid(self, form):
        nombre = form.cleaned_data.get('nombre').lower()
        response = super().form_valid(form)
        success_url = reverse('app:agente_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class AgenteDeleteView(DeleteView):
    model = Agente
    template_name = 'agente/eliminar.html'
    success_url = reverse_lazy('app:agente_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar agente'
        context['entidad'] = 'Eliminar agente'
        context['listar_url'] = reverse_lazy('app:agente_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Agente eliminado con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el agente.'})