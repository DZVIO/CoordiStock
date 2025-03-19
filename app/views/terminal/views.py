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
from app.models import Terminal
from app.forms import TerminalForm

@method_decorator(never_cache, name='dispatch')
def lista_terminal(request):
    nombre = {
        'titulo': 'Listado de terminales',
        'terminales': Terminal.objects.all()
    }
    return render(request, 'terminal/listar.html',nombre)

###### LISTAR ######

@method_decorator(never_cache, name='dispatch')
class TerminalListView(ListView):
    model = Terminal
    template_name = 'terminal/listar.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Juan'}
        return JsonResponse(nombre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de terminales'
        context['entidad'] = 'Listado de terminales'
        context['listar_url'] = reverse_lazy('app:terminal_lista')
        context['crear_url'] = reverse_lazy('app:terminal_crear')
        return context

###### CREAR ######
@method_decorator(never_cache, name='dispatch')
class TerminalCreateView(CreateView):
    model = Terminal
    form_class = TerminalForm
    template_name = 'terminal/crear.html'
    success_url = reverse_lazy('app:terminal_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar terminal'
        context['entidad'] = 'Registrar terminal'
        context['listar_url'] = reverse_lazy('app:terminal_lista')
        return context
    
    def form_valid(self, form):
        terminal = form.cleaned_data.get('terminal').lower()
        
        if Terminal.objects.filter(terminal__iexact=terminal).exists():
            form.add_error('terminal', 'Ya existe una terminal registrada con ese nombre.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        success_url = reverse('app:terminal_crear') + '?created=True'
        return redirect(success_url)

###### EDITAR ######

@method_decorator(never_cache, name='dispatch')
class TerminalUpdateView(UpdateView):
    model = Terminal
    form_class = TerminalForm
    template_name = 'terminal/crear.html'
    success_url = reverse_lazy('app:terminal_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar terminal'
        context['entidad'] = 'Editar terminal'
        context['error'] = 'Esta terminal ya existe'
        context['listar_url'] = reverse_lazy('app:terminal_lista')
        return context

    def form_valid(self, form):
        terminal = form.cleaned_data.get('terminal').lower()
        response = super().form_valid(form)
        success_url = reverse('app:terminal_crear') + '?updated=True'
        return redirect(success_url)

###### ELIMINAR ######

@method_decorator(never_cache, name='dispatch')
class TerminalDeleteView(DeleteView):
    model = Terminal
    template_name = 'terminal/eliminar.html'
    success_url = reverse_lazy('app:terminal_lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar terminal'
        context['entidad'] = 'Eliminar terminal'
        context['listar_url'] = reverse_lazy('app:terminal_lista')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'success': True, 'message': 'Terminal eliminada con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar la terminal.'})