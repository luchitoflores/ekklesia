# -*- coding:utf-8 -*-

# Core de Python
import json
import operator

# Librerías de Django
from django.db.models import Q
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect

# Librerías de terceros
from tastypie.resources import ModelResource

# Librerías del proyecto
from .forms import PerfilUsuarioForm, UsuarioForm, PadreForm,NotaMarginalForm, UsuarioPadreForm
from .models import (PerfilUsuario,NotaMarginal,Bautismo,Matrimonio,
	Parroquia)


# Api parroquias
class ParroquiaResource(ModelResource):
	class Meta:
		queryset = Parroquia.objects.all()
		resource_name = 'parroquia' 
		fields = ('id', 'nombre')
		allowed_methods = ['get']



# Método para crear un feligres
def usuarioCreateAjax(request):
	if request.method == 'POST':
		bandera = False
		usuario_form = UsuarioForm(request.POST)
		perfil_form = PerfilUsuarioForm(request.POST)
		if usuario_form.is_valid() and perfil_form.is_valid():
			usuario_form.save()
			perfil_form.save()
			bandera = True




# Método para crear el padre o madre de un feligres - está funcionando
def padre_create_ajax(request):
	sexo = request.POST.get('sexo')
	if request.method == 'POST':
		respuesta = False
		usuario_form = UsuarioPadreForm(request.POST)
		perfil_form = PadreForm(request.POST)
		if usuario_form.is_valid() and perfil_form.is_valid():
			perfil = perfil_form.save(commit=False)
			usuario = usuario_form.save(commit=False)
			usuario.username = perfil.crear_username(usuario.first_name, usuario.last_name)
			usuario.set_password(usuario.username)
			feligres, created = Group.objects.get_or_create(name='Feligres')
			usuario.save()
			usuario.groups.add(feligres)
			perfil.user = usuario
			if sexo:
				perfil.sexo = sexo
			perfil.save()
			respuesta = True
			ctx = {'respuesta': respuesta, 'id': perfil.user.id, 
			'full_name': perfil.user.get_full_name()}
		else:
			errores_usuario = usuario_form.errors
			errores_perfil =  perfil_form.errors
			ctx = {'respuesta': False, 'errores_usuario':errores_usuario,
			 'errores_perfil': errores_perfil}

	return HttpResponse(json.dumps(ctx), content_type='application/json')


# vista para crear una nota marginal a Bautismo con modal.....
def nota_marginal_create_ajax(request):
	
	if request.method == 'POST':
		respuesta = False
		form_nota = NotaMarginalForm(request.POST)
		bautismo_id=request.POST.get('id')

		if bautismo_id!=None and form_nota.is_valid():
			bautismo=Bautismo.objects.get(pk=bautismo_id)
			nota=form_nota.save(commit=False)
			nota.bautismo=bautismo
			nota.save()
			respuesta = True
			notas=NotaMarginal.objects.filter(bautismo=bautismo).order_by('-fecha')
			lista=list()
			for nota in notas:
				lista.append({'tabla':'<tr><th> %s</th><th> %s</th></tr>'%(nota.fecha ,nota.descripcion)})
			ctx = {'respuesta': respuesta, 'tabla':lista}
		else:
			errores_nota = form_nota.errors
			ctx = {'respuesta': False, 'errores_nota':errores_nota}

	return HttpResponse(json.dumps(ctx), content_type='application/json')


# vista para crear una nota marginal a Matrimonio con modal.....

def nota_create_matrimonio_ajax(request):
	
	if request.method == 'POST':
		respuesta = False
		form_nota = NotaMarginalForm(request.POST)
		matrimonio_id=request.POST.get('id')

		if matrimonio_id!=None and form_nota.is_valid():
			matrimonio=Matrimonio.objects.get(pk=matrimonio_id)
			nota=form_nota.save(commit=False)
			nota.matrimonio=matrimonio
			nota.save()
			respuesta = True
			notas=NotaMarginal.objects.filter(matrimonio=matrimonio).order_by('-fecha')
			lista=list()
			for nota in notas:
				lista.append({'tabla':'<tr><th> %s</th><th> %s</th></tr>'%(nota.fecha ,nota.descripcion)})
			ctx = {'respuesta': respuesta, 'tabla':lista}
		else:
			errores_nota = form_nota.errors
			ctx = {'respuesta': False, 'errores_nota':errores_nota}

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



# def buscar_usuarios(request):
# 	nombres = request.GET.get('nombres')
# 	apellidos = request.GET.get('apellidos')
# 	cedula = request.GET.get('cedula')
# 	lista = list()
# 	bandera = False
	
# 	if cedula:
# 		try:
# 			perfil = PerfilUsuario.objects.get(dni=cedula)
# 			bandera = True
# 			lista.append({'id': perfil.id , 'dni': perfil.dni, 'link': '<a id="id_click" href=".">'+perfil.user.first_name+'</a>', 'nombres': perfil.user.first_name, 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil, "DT_RowId":perfil.id})
# 			ctx={'perfiles':lista, 'bandera': bandera}
			
# 		except Exception:
# 			bandera=False
# 			ctx={'perfiles':lista, 'bandera': bandera}

# 	elif nombres or apellidos:
# 		try:
# 			bandera = True
# 			perfiles = PerfilUsuario.objects.filter(user__last_name__contains= apellidos, user__first_name__contains=nombres)
# 			if len(perfiles) > 0:
# 				perfiles.distinct().order_by('user__last_name', 'user__first_name' )
# 				for perfil in perfiles:
# 					lista.append({'id': perfil.id , 'dni': perfil.dni, 'link': '<a id="id_click" href=".">'+perfil.user.first_name+'</a>', 'nombres': perfil.user.first_name, 'apellidos': perfil.user.last_name, 'lugar_nacimiento': perfil.lugar_nacimiento, 'profesion':perfil.profesion, 'estado_civil': perfil.estado_civil, "DT_RowId":perfil.id})
# 				ctx={'perfiles':lista, 'bandera': bandera}
# 			else:
# 				bandera = False
# 				ctx={'perfiles':lista, 'bandera': bandera}
			
# 		except Exception:
# 			bandera=False
# 			ctx={'perfiles': lista, 'bandera': bandera}
# 	else:
# 		bandera=False
# 		ctx={'perfiles':lista, 'bandera': bandera}
# 	return HttpResponse(json.dumps(ctx), content_type='application/json')




def edit_padre_viewapi(request):
	idpadre = request.POST.get('idpadre')
	idfeligres = request.POST.get('idfeligres')
	
	try:
		padre = PerfilUsuario.objects.get(id=idpadre)
		feligres = PerfilUsuario.objects.get(pk=idfeligres)
		feligres.padre = padre.user
		feligres.save()
		ctx = {'bandera': True}
		return HttpResponseRedirect('/usuario')
	except Exception:
		ctx = {'bandera': False}
	return HttpResponse(json.dumps(ctx), content_type='applcation/json')

def data_tables(request):
	iTotalRecords = PerfilUsuario.objects.all().count() # Indica el número total de registros en la BD
	iTotalDisplayRecords = 1 #Indica el número total de registros que se mostrarán en la tabla al hacer una búsqueda
	iDisplayLength = request.GET.get('iDisplayLength') # Obtiene el numero de registros que van a ser mostrados de un intervalo [5, 10, 25, Todos]
	q = request.GET.get('sSearch').split() # Me devuelve el criterio de búsqueda que pongo en el input de búsqueda
	sEcho = request.GET['sEcho'] #indica el número de peticiones que se ha hecho al servidor
	lista = list()
	iSortingCols = request.GET['iSortingCols'] #Numero de columnas ordenables
	
	ordenacion = ''
	sColumns = request.GET.get('sColumns').split(',')

	 #Devuelve el nombre de las columnas separadas por comas
	lista_ordenacion = []
	for i in iSortingCols:
		columna_ordenable = 'bSortable_%d' % int(i)
		columna = request.GET[columna_ordenable] # devuelve verdadero si la columna es ordenable y falso si pasa lo contrario
		if columna:
			pass
			# cadena_ordenacion = 'iSortCol_%d' % int(i) # sSortDir devuelve una cadena asc o desc
			# tipo_ordenacion = request.GET[cadena_ordenacion]
			# lista_ordenacion.append[sColumns[int(i)]]

			# if tipo_ordenacion == 'asc':
			# 	pass
			# else:
			# 	pass


	# iSortingCols = request.GET['iSortingCols'] # las columnas a ordenar
	# print q
	# q = 'Luis'
	if q:
		query = reduce(operator.__or__, [Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(dni=q) for q in q])
		perfiles = PerfilUsuario.objects.filter(query).distinct().order_by('user__first_name', 'user__last_name')[:2]
		iTotalDisplayRecords = perfiles.count()
	else:
		perfiles = PerfilUsuario.objects.filter(user__first_name='Jose')	
	for perfil in perfiles:
		lista.append({'Nombres': perfil.user.first_name, 'Dni': perfil.dni,"DT_RowId":perfil.id})
	
	ctx = { "sEcho": sEcho, "iTotalRecords": iTotalRecords,"iTotalDisplayRecords": iTotalDisplayRecords,"aaData": lista}
	# print lista
	return HttpResponse(json.dumps(ctx), content_type='application/json')