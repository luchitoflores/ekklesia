# -*- coding:utf-8 -*-
import json
import operator

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

from .forms import PerfilUsuarioForm, UsuarioForm, PadreForm
from .models import PerfilUsuario

# Método para crear el padre o madre de un feligres - está funcionando
def padre_create_ajax(request):
	sexo = request.POST.get('sexo')
	if request.method == 'POST':
		respuesta = False
		usuario_form = UsuarioForm(request.POST)
		perfil_form = PadreForm(request.POST)
		if usuario_form.is_valid() and perfil_form.is_valid():
			perfil = perfil_form.save(commit=False)
			usuario = usuario_form.save(commit=False)
			usuario.username = '%s' % perfil.dni
			usuario.save()
			perfil.user = usuario
			if sexo:
				perfil.sexo = sexo
			perfil.save()
			respuesta = True
			ctx = {'respuesta': respuesta, 'id': perfil.user.id, 'full_name': perfil.user.get_full_name()}
		else:
			errores_usuario = usuario_form.errors
			errores_perfil =  perfil_form.errors
			ctx = {'respuesta': False, 'errores_usuario':errores_usuario, 'errores_perfil': errores_perfil}

	return HttpResponse(json.dumps(ctx), content_type='application/json')


#Esta función permite buscar usuarios mediante ajax --- sirve para autocomplete y las listas
# No hay que borrarla porque es una función muy importante
# def buscar_usuarios(request):
# 	q = request.GET.get('q')
# 	lista = list()
# 	bandera = False
# 	if q:
# 		query = reduce(operator.__or__, [Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(dni=q) for q in q])
# 		perfiles = PerfilUsuario.objects.filter(query).distinct()
# 		if len(perfiles) > 0:
# 			perfiles.distinct().order_by('user__last_name', 'user__first_name' )
# 			for perfil in perfiles:
# 				lista.append({'id': perfil.id , 'dni': perfil.dni, 'link': '<a id="id_click" href=".">'+perfil.user.first_name+'</a>', 'nombres': perfil.user.first_name, 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil, "DT_RowId":perfil.id})
# 			ctx={'perfiles':lista, 'bandera': bandera}
# 		else:
# 			bandera = False
# 			ctx={'perfiles':lista, 'bandera': bandera}
# 	else:
# 		bandera=False
# 		ctx={'perfiles':lista, 'bandera': bandera}
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
			lista.append({'id': perfil.id , 'dni': perfil.dni, 'link': '<a id="id_click" href=".">'+perfil.user.first_name+'</a>', 'nombres': perfil.user.first_name, 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil, "DT_RowId":perfil.id})
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
					lista.append({'id': perfil.id , 'dni': perfil.dni, 'link': '<a id="id_click" href=".">'+perfil.user.first_name+'</a>', 'nombres': perfil.user.first_name, 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil, 'sexo': perfil.sexo, "DT_RowId":perfil.id})
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


# Esta funcion estaba funcionando con el plugin de datatables

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



		




