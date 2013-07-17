# Create your views here.
import json

from django.shortcuts import render
from django.http import HttpResponse, Http404


from .forms import UsuarioForm, PerfilUsuarioForm

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
<<<<<<< HEAD
	a=5
	b=1222


def prueba2(request):

	a=1
	b=12
	if(a==1):
		a=a+b
	a=5
	b=1222


def pruebaconflictos github(request):

	a=1
	b=12
	if(a==1):
		a=a+b
	a=5
	b=1222
=======

	a=5
	b=1222
	b=b*a


def crearPrueba(request):
	a=34+45
	return a
>>>>>>> 4ebb01497efbbc64d11f8b7cd524fd6f4a221018

