import json

from django.http import HttpResponse

from .forms import PerfilUsuarioForm, UsuarioForm

def usuarioCreateAjax(request):
	if request.method == 'POST':
		bandera = False
		usuario_form = UsuarioForm(request.POST)
		perfil_form = PerfilUsuarioForm(request.POST)
		if usuario_form.is_valid() and perfil_form.is_valid():
			usuario_form.save()
			perfil_form.save()
			bandera = True

	ctx = {'respuesta': bandera}
	return HttpResponse(json.dumps(ctx), content_type='application/json')

