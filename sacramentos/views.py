# Create your views here.
import json

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView


from .forms import UsuarioForm, PerfilUsuarioForm, LibroForm
from .models import Libro

def usuarioCreateView(request):
	if request.is_ajax():
		if request.method == 'POST':
			bandera = False
			usuario_form = UsuarioForm(request.POST)
			perfil_form = PerfilUsuarioForm(request.POST)
			# if usuario_form.is_valid() and perfil_form.is_valid():
			bandera = True
			usuario = usuario_form.save(commit=False)
			perfil = perfil_form.save(commit=False)
			usuario.username = '%s%s%s' %(usuario.first_name, usuario.last_name, perfil.dni)
			usuario.save()
			perfil.user = usuario
			perfil.save()
			
			ctx = {'respuesta': bandera}
			return HttpResponse(json.dumps(ctx), content_type='application/json')
	else:
		usuario_form = UsuarioForm()
		perfil_form = PerfilUsuarioForm()
		ctx = {'usuario_form': usuario_form, 'perfil_form': perfil_form}
		return render (request, 'usuario/usuario_form.html', ctx)


def prueba(request):
	a=1
	b=12
	if(a==1):
		a=a+b

	a=5
	b=1222


def prueba2(request):
	a=1
	b=12
	if(a==1):
		a=a+b
	a=5
	b=1222





def crearPrueba(request):
	a=34+45
	return a


def crearPrueba(request):
	a=34+45
	return a


# Vistas para admin libros

class LibroCreateView(CreateView):
	model = Libro
	form_class = LibroForm
	template_name = 'libro/libro_form.html'
	success_url= '/libro/'

class LibroUpdateView(UpdateView):
	model = Libro
	form_class=LibroForm
	template_name = 'libro/libro_form.html'
	success_url = '/libro/'

class LibroListView(ListView):
	model = Libro
	template_name = 'libro/libro_list.html'
	# paginate_by = 5
	# def get_queryset(self):
	# 	queryset=super(LibroListView, self).get_queryset()
	# 	query = self.request.GET.get('q')
	# 	if query:
	# 		return queryset.filter(tipo_libro__icontains=query)
	# 	return queryset

	