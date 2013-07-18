# Create your views here.
import json

from django.shortcuts import render
from django.http import HttpResponse, Http404


from .forms import UsuarioForm, PerfilUsuarioForm, PadreForm

def usuarioCreateView(request):
	if request.is_ajax():
		if request.method == 'POST':
			valido = False
			usuario_form = UsuarioForm(request.POST)
			perfil_form = PerfilUsuarioForm(request.POST)
			if usuario_form.is_valid() and perfil_form.is_valid():
				valido = True
				usuario = usuario_form.save(commit=False)
				perfil = perfil_form.save(commit=False)
				usuario.username = '%s%s%s' %(usuario.first_name, usuario.last_name, perfil.dni)
				usuario.save()
				perfil.user = usuario
				perfil.save()
				ctx = {'valido': valido}

			else:
				errores_usuario = usuario_form.errors
				errores_perfil =  perfil_form.errors
				ctx = {'valido': valido, 'errores_usuario':errores_usuario, 'errores_perfil': errores_perfil}

			return HttpResponse(json.dumps(ctx), content_type='application/json')
	else:
		usuario_form = UsuarioForm()
		perfil_form = PerfilUsuarioForm()
		ctx = {'usuario_form': usuario_form, 'perfil_form': perfil_form}
		return render (request, 'usuario/usuario_form.html', ctx)


def padre_create_view(request):
	if request.is_ajax():
		if request.method == 'POST':
			usuario_form = UsuarioForm(request.POST)
			perfil_padre_form = PadreForm(request.POST)
			if usuario_form.is_valid() and perfil_padre_form.is_valid():
				pass
	else: 
		usuario_form = UsuarioForm()
		perfil_padre_form = PadreForm()

	ctx = {'usuario_form': usuario_form, 'perfil_form': perfil_padre_form}
	return render(request, 'usuario/padre_form.html', ctx) 







