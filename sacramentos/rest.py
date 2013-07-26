# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http import HttpResponse

from .forms import PerfilUsuarioForm, UsuarioForm
from .models import PerfilUsuario

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

# def api_usuario_list(request):
# 	sEcho = request.GET['sEcho']
# 	iDisplayStart = request.GET['iDisplayStart']
# 	iDisplayLength = request.GET['iDisplayLength']
# 	sSearch = request.GET.get('sSearch')
# 	iSortingCols = request.GET['iSortingCols'] # las columnas a ordenar
# 	iTotalRecords = 0
# 	iSortCol = list()
# 	lista = list()
# 	ordenacion = '%s%s%s%s%s' % ('dni', '"', ',', '"', 'dni')

# 	if sSearch:
# 		feligreses = PerfilUsuario.objects.filter(
# 			Q(user__first_name__icontains=sSearch) |
# 			Q(user__last_name__icontains=sSearch) |
# 			Q(dni=sSearch) |
# 			Q(lugar_nacimiento=sSearch)
# 			)

# 		feligreses = feligreses.order_by(dni)
# 		for feligres in feligreses:
# 			lista.append({'Nombres': feligres.user.first_name, 'Apellidos': feligres.user.last_name, 'Dni': feligres.lugar_nacimiento,'Prueba':sSearch,"DT_RowId":feligres.id})
# 			iTotalRecords = feligreses.count()
	
# 	if iSortingCols > 0:
# 		pass


# 	ctx = {"sEcho": sEcho,"iTotalRecords": iTotalRecords,"iTotalDisplayRecords": iTotalRecords,"aaData": lista}
# 	return HttpResponse(json.dumps(ctx), content_type='application/json')


def buscar_usuarios(request):
	nombres = request.GET.get('nombres')
	apellidos = request.GET.get('apellidos')
	cedula = request.GET.get('cedula')
	lista = list()
	bandera = False
	
	if cedula:
		try:
			perfil = PerfilUsuario.objects.get(dni=cedula)
			bandera = True
			lista.append({'id': perfil.id , 'dni': perfil.dni, 'nombres': '<a href="">'+perfil.user.first_name+'</a>', 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil})
			ctx={'perfiles':lista, 'bandera': bandera}
			
		except Exception:
			bandera=False
			ctx={'perfiles':lista, 'bandera': bandera}

	elif nombres or apellidos:
		try:
			bandera = True
			perfiles = PerfilUsuario.objects.filter(user__last_name__contains= apellidos, user__first_name__contains=nombres)
			if len(perfiles) > 0:
				perfiles.distinct().order_by('user__last_name', 'user__first_name' )
				for perfil in perfiles:
					lista.append({'id': perfil.id , 'dni': perfil.dni, 'nombres': '<a href="">'+perfil.user.first_name+'</a>', 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil})
				ctx={'perfiles':lista, 'bandera': bandera}
			else:
				bandera = False
				ctx={'perfiles':lista, 'bandera': bandera}
			
		except Exception:
			bandera=False
			ctx={'perfiles': lista, 'bandera': bandera}
	else:
		bandera=False
		ctx={'perfiles':lista, 'bandera': bandera}
	return HttpResponse(json.dumps(ctx), content_type='application/json')

def buscar_usuario_cedula(request):
	q = request.GET.get('q', '')
	if q:
		try:
			perfil = PerfilUser.objects.get(dni=q)
			lista = list()
			lista.append({'id': perfil.id , 'dni': perfil.dni, 'nombres': perfil.user.first_name, 'apellidos': perfil.user.last_name })
			ctx={'perfil':lista}
			
		except Exception:
			ctx={'perfil': False}
	else:
		ctx={'perfil':'Debe ingresar un criterio de busqueda'}

	return HttpResponse(json.dumps(ctx), content_type='application/json')

