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

<<<<<<< HEAD





=======
def prueba(request):

	a=1
	b=12
	if(a==1):
		a=a+b
<<<<<<< HEAD
>>>>>>> 24dbdc27ed52cc2c7ebc9cfeaca8cd5ba3088b1a
=======
	a=5
	b=1222
<<<<<<< HEAD
	b=b*a


def crearPrueba(request):
	a=34+45
	return a
=======
>>>>>>> 666a47ddb63fb56489a934b20f89e297f8c55c18
>>>>>>> 78016cef93a53bc492088a7d6a62934da9c12924
