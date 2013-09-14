# -*- coding:utf-8 -*-
# Create your views here.
import json
import csv
from datetime import datetime
from datetime import date
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render,get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView
# Para los logs
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
# 
from ho import pisa
import StringIO 
import cgi

from .models import (PerfilUsuario,
	Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,NotaMarginal,
	Parroquia, Intenciones,
	AsignacionParroquia, PeriodoAsignacionParroquia,
	)

from .forms import (
	UsuarioForm, UsuarioPadreForm, UsuarioSacerdoteForm, PerfilUsuarioForm, PadreForm, SacerdoteForm, 
	MatrimonioForm,MatrimonioFormEditar,
	BautismoForm,BautismoFormEditar,
	EucaristiaForm,EucaristiaFormEditar,
	ConfirmacionForm,ConfirmacionFormEditar,
	LibroForm,NotaMarginalForm,
	DivErrorList,
	IntencionForm,
	ParroquiaForm, 
	AsignarParroquiaForm, PeriodoAsignacionParroquiaForm, 
	AsignarSecretariaForm,
	ReporteIntencionesForm,ReporteSacramentosAnualForm,ReportePermisoForm,
	)

from ciudades.forms import DireccionForm
from ciudades.models import Canton, Provincia, Parroquia as ParroquiaCivil


@login_required(login_url='/login/')
def usuarioCreateView(request):
	if request.method == 'POST':
		form_usuario = UsuarioForm(request.POST)
		padre = PerfilUsuario.objects.padre()
		madre =  PerfilUsuario.objects.madre()
		form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
		
		if form_usuario.is_valid() and form_perfil.is_valid():
			feligres, created = Group.objects.get_or_create(name='Feligres')
			usuario = form_usuario.save(commit=False)
			perfil = form_perfil.save(commit=False)
			usuario.username = perfil.crear_username(usuario.first_name, usuario.last_name)
			usuario.set_password(usuario.username)
			usuario.save()
			usuario.groups.add(feligres)
			perfil.user = usuario
			perfil.save()
			return HttpResponseRedirect('/usuario')
			
		else:
			padre = request.POST.get('padre')
			madre =  request.POST.get('madre')

			if padre and madre:
				padre = PerfilUsuario.objects.filter(id=padre)
				madre = PerfilUsuario.objects.filter(id=madre)
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
			elif padre and not madre:
				padre = PerfilUsuario.objects.filter(id=padre)
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
			elif not padre and madre:
				madre = PerfilUsuario.objects.filter(id=madre)
				padre= PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)

			else:
				padre = PerfilUsuario.objects.none()
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
			
			messages.error(request, 'Uno o más datos no son válidos')
			ctx = {'form_usuario': form_usuario , 'form_perfil': form_perfil}
			return render (request, 'usuario/usuario_form.html', ctx)
	else:
		form_usuario = UsuarioForm()
		form_perfil = PerfilUsuarioForm(label_suffix=':')
		# form_perfil.fields['madre'] = forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), required=False, empty_label='--- Seleccione ---')
		# form_perfil.fields['padre'] = forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), required=False, empty_label='--- Seleccione ---')
		ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil}
		return render (request, 'usuario/usuario_form.html', ctx)

@login_required(login_url='/login/')
def edit_usuario_view(request,pk):
	perfil= get_object_or_404(PerfilUsuario, pk=pk)
	user= perfil.user	
	if request.method == 'POST':
		padre = PerfilUsuario.objects.padre()
		madre =  PerfilUsuario.objects.madre()
		form_usuario = UsuarioForm(request.POST,instance=user)
		form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
		if form_usuario.is_valid() and form_perfil.is_valid():
			form_usuario.save()
			form_perfil.save()
			return HttpResponseRedirect('/usuario')
		else:
			if perfil.padre and perfil.madre:
				padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
				madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
			elif perfil.padre and not perfil.madre:
				padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
			elif not perfil.padre and perfil.madre:
				madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
				padre= PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)

			else:
				padre = PerfilUsuario.objects.none()
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
			
			messages.error(request, 'Uno o más campos no son válidos')
			ctx = {'form_usuario': form_usuario,'form_perfil':form_perfil, 'perfil':perfil}
			return render(request, 'usuario/usuario_form.html', ctx)

	else:
		if perfil.padre and perfil.madre:
			padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
			madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
			form_perfil = PerfilUsuarioForm(padre, madre, instance=perfil)
		elif perfil.padre and not perfil.madre:
			padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
			form_perfil = PerfilUsuarioForm(padre, instance=perfil)
		elif not perfil.padre and perfil.madre:
			madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
			padre= PerfilUsuario.objects.none()
			form_perfil = PerfilUsuarioForm(padre, madre, instance=perfil)

		else:
			form_perfil = PerfilUsuarioForm(instance=perfil)

		form_usuario = UsuarioForm(instance=user)
		
									
	ctx = {'form_usuario': form_usuario,'form_perfil':form_perfil, 'perfil':perfil}
	return render(request, 'usuario/usuario_form.html', ctx)

class UsuarioListView(ListView):
	model=User
	model=PerfilUsuario
	template_name="usuario/usuario_list.html"
	queryset = PerfilUsuario.objects.feligres()

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(UsuarioListView, self).dispatch(*args, **kwargs)

		
@login_required
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

@login_required
def feligres_create_view(request):
	if request.method == 'POST':
		usuario_form = UsuarioPadreForm(request.POST)
		perfil_form = PerfilUsuarioForm(request.POST)
		if usuario_form.is_valid() and perfil_form.is_valid():
			pass
	else: 
		usuario_form = UsuarioForm()
		perfil_form = PerfilUsuarioForm()

	ctx = {'usuario_form': usuario_form, 'perfil_form': perfil_form}
	return render(request, 'usuario/feligres.html', ctx) 


@login_required(login_url='/login/')
@permission_required('sacramentos.can_change', login_url='/login/')
def sacerdote_create_view(request):
	template_name = 'usuario/sacerdote_form.html' 
	success_url = '/sacerdote/'
	if request.method == 'POST':
		form_sacerdote = SacerdoteForm(request.POST)
		form_usuario = UsuarioSacerdoteForm(request.POST)
		if form_sacerdote.is_valid() and form_usuario.is_valid():
			sacerdotes, created = Group.objects.get_or_create(name='Sacerdote')
			usuario = form_usuario.save(commit= False) 
			sacerdote = form_sacerdote.save(commit=False)
			usuario.username= sacerdote.crear_username(usuario.first_name, usuario.last_name)
			usuario.set_password(usuario.username)
			usuario.save()
			usuario.groups.add(sacerdotes)
			sacerdote.user =usuario
			sacerdote.sexo = 'm'
			sacerdote.profesion = 'Sacerdote'
			sacerdote.estado_civil = 's'
			sacerdote.save()
			return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Uno o más datos son inválidos')
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
			return render(request, template_name, ctx)

	else:
		form_sacerdote = SacerdoteForm()
		form_usuario = UsuarioSacerdoteForm()
		ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
def sacerdote_update_view(request, pk):
	sacerdote = get_object_or_404(PerfilUsuario, pk=pk)
	if sacerdote.profesion != 'Sacerdote':
		raise Http404
	else: 
		template_name = 'usuario/sacerdote_form.html' 
		success_url = '/sacerdote/'
		if request.method == 'POST':
			form_sacerdote = SacerdoteForm(request.POST, instance=sacerdote)
			form_usuario = UsuarioSacerdoteForm(request.POST, instance=sacerdote.user)
			if form_sacerdote.is_valid() and form_usuario.is_valid():
				usuario = form_usuario.save() 
				sacerdote = form_sacerdote.save()
				# usuario.save()
				# sacerdote.save()
				return HttpResponseRedirect(success_url)

			else:
				messages.error(request, 'Uno o más datos son inválidos')
				ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
				return render(request, template_name, ctx)

		else:
			form_sacerdote = SacerdoteForm(instance=sacerdote)
			form_usuario = UsuarioSacerdoteForm(instance=sacerdote.user)
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
			return render(request, template_name, ctx)


class SacerdoteListView(ListView):
	model = PerfilUsuario
	template_name = 'usuario/sacerdote_list.html'
	queryset = PerfilUsuario.objects.sacerdote()

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.can_change', login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(SacerdoteListView, self).dispatch(*args, **kwargs)






# Vistas para admin libros

# class LibroCreateView(CreateView):
# 	model = Libro
# 	form_class = LibroForm
# 	template_name = 'libro/libro_form.html'
# 	success_url= '/libro/'
def libro_create_view(request):
	if(request.method=='POST'):
		form_libro=LibroForm(request.POST)
		if form_libro.is_valid():
			libro=form_libro.save(commit=False)
			estado=libro.estado
			tipo=libro.tipo_libro
			asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user)
			# periodos = PeriodoAsignacionParroquia.objects.get(asignacion=asignacion, estado=True)
			libro.parroquia = asignacion.parroquia

			try:

				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,
					parroquia=asignacion.parroquia)
				if(estado != consulta.estado and tipo!=consulta.tipo_libro):
					libro.save()
					LogEntry.objects.log_action(
            		user_id=request.user.id,
            		content_type_id=ContentType.objects.get_for_model(libro).pk,
            		object_id=libro.id,
            		object_repr=unicode(libro.tipo_libro),
            		action_flag=ADDITION,
            		change_message="Creo un libro")
					messages.success(request, 'Creado exitosamente')
					return HttpResponseRedirect('/libro')
					

				elif(estado != consulta.estado and tipo==consulta.tipo_libro):
					libro.save()
					LogEntry.objects.log_action(
            		user_id=request.user.id,
            		content_type_id=ContentType.objects.get_for_model(libro).pk,
            		object_id=libro.id,
            		object_repr=unicode(libro.tipo_libro),
            		action_flag=ADDITION,
            		change_message="Creo un libro")
					messages.success(request, 'Creado exitosamente')
					return HttpResponseRedirect('/libro')
					
				else:

					messages.info(request,'Ya existe un libro abierto, cierrelo '+
						'y vuela a crear')
					# messages.add_message(request,messages.WARNING,
					# 	{'Libro':'Ya existe un libro abierto, cierrelo y vuela a crear'})

			except ObjectDoesNotExist:
				libro.save()
				LogEntry.objects.log_action(
            			user_id=request.user.id,
            			content_type_id=ContentType.objects.get_for_model(libro).pk,
            			object_id=libro.id,
            			object_repr=unicode(libro.tipo_libro),
            			action_flag=ADDITION,
            			change_message="Creo un libro")
				messages.success(request, 'Creado exitosamente')
				return HttpResponseRedirect('/libro')
				

		else:
			messages.error(request,'Uno o mas datos son invalidos')
			# messages.add_message(request,messages.WARNING,{'libro':form_libro.errors})
	else:
		form_libro=LibroForm()
	ctx={'form_libro':form_libro}
	return render(request,'libro/libro_form.html',ctx)


# class LibroUpdateView(UpdateView):
# 	model = Libro
# 	form_class=LibroForm
# 	template_name = 'libro/libro_form.html'
# 	success_url = '/libro/'

def libro_update_view(request,pk):
	libros=get_object_or_404(Libro,pk=pk)
	
	if(request.method=='POST'):
		form_libro=LibroForm(request.POST,instance=libros)
		if(form_libro.is_valid()):
			libro=form_libro.save(commit=False)
			estado=libro.estado
			tipo=libro.tipo_libro
			asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user)
			try:
				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,
					parroquia=asignacion.parroquia)
				if (libro.id == consulta.id):
					if libro.estado == consulta.estado:
						libro.save()
						LogEntry.objects.log_action(
            			user_id=request.user.id,
            			content_type_id=ContentType.objects.get_for_model(libro).pk,
            			object_id=libro.id,
            			object_repr=unicode(libro.tipo_libro),
            			action_flag=CHANGE,
            			change_message="actualizo un libro")
						messages.success(request, 'Actualizado exitosamente')
						return HttpResponseRedirect('/libro')
					else:
						libro.save()
						LogEntry.objects.log_action(
            			user_id=request.user.id,
            			content_type_id=ContentType.objects.get_for_model(libro).pk,
            			object_id=libro.id,
            			object_repr=unicode(libro.tipo_libro),
            			action_flag=CHANGE,
            			change_message="actualizo un libro")
						messages.success(request, 'Actualizado exitosamente')
						return HttpResponseRedirect('/libro')
						
				else:


					if(estado != consulta.estado and tipo!=consulta.tipo_libro):
						libro.save()
						LogEntry.objects.log_action(
            			user_id=request.user.id,
            			content_type_id=ContentType.objects.get_for_model(libro).pk,
            			object_id=libro.id,
            			object_repr=unicode(libro.tipo_libro),
            			action_flag=CHANGE,
            			change_message="actualizo un libro")
						messages.success(request, 'Actualizado exitosamente')
						return HttpResponseRedirect('/libro')
						
					elif(estado != consulta.estado and tipo==consulta.tipo_libro):
						libro.save()
						LogEntry.objects.log_action(
            			user_id=request.user.id,
            			content_type_id=ContentType.objects.get_for_model(libro).pk,
            			object_id=libro.id,
            			object_repr=unicode(libro.tipo_libro),
            			action_flag=CHANGE,
            			change_message="actualizo un libro")
						messages.success(request, 'Actualizado exitosamente')
						return HttpResponseRedirect('/libro')
													
					else:

						messages.info(request,'Ya existe un libro abierto, cierrelo '+
							'y vuela a crear')
						# messages.add_message(request,messages.WARNING,
						# 	{'Libro':'Ya existe un libro abierto, cierrelo y vuela a crear'})

			except ObjectDoesNotExist:
				
				libro.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
            		content_type_id=ContentType.objects.get_for_model(libro).pk,
            		object_id=libro.id,
            		object_repr=unicode(libro.tipo_libro),
            		action_flag=CHANGE,
            		change_message="actualizo un libro")
				messages.success(request, 'Actualizado exitosamente')
				return HttpResponseRedirect('/libro')
		else:
			
			messages.error(request,'Uno o mas datos son invalidos')
			ctx={'form_libro':form_libro,'object':libros}
			return render(request,'libro/libro_form.html',ctx)
	else:
		
		form_libro=LibroForm(instance=libros)

	ctx={'form_libro':form_libro,'object':libros}
	return render(request,'libro/libro_form.html',ctx)


class LibroListView(ListView):
	model = Libro
	template_name = 'libro/libro_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user)
			queryset = Libro.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];
	
class LibroListJson(BaseDatatableView):
	# order_columns = ['numero_libro', 'tipo_libro', 'fecha_apertura']
	
	# def render_column(self, row, column):
	# 	if column == 'numero_libro':
	# 		return '%s %s' % (row.tipo_libro, row.numero_libro)
	# 	else:
	# 		return super(Libro, self).render_column(row, column)
	
	def filter_queryset(self, qs):
		parroquia = AsignacionParroquia.objects.get(persona__user=self.request.user).parroquia
		print(parroquia)
		sSearch = self.request.POST.get('sSearch', None)
		if sSearch:
			qs = qs.filter(Q(numero_libro__contains=sSearch,parroquia=parroquia)|
				Q(tipo_libro__contains=sSearch,parroquia=parroquia))
		return qs
		print(qs)

	def prepare_results(self, qs):
		json_data = []
		for accession in qs:
			json_data.append([
				accession.numero_libro,
				accession.tipo_libro,
				accession.fecha_apertura,
				accession.fecha_cierre,
				accession.estado
				])
		return json_data
		print('json_data %s'%json_data)

		# filter_customer = self.request.POST.get('customer', None)
		# if filter_customer:
		# 	customer_parts = filter_customer.split(' ')
		# 	qs_params = None
		# 	for part in customer_parts:
		# 		q = Q(customer_firstname__istartswith=part,parroquia=parroquia)|Q(customer_lastname__istartswith=part,parroquia=parroquia)
		# 		qs_params = qs_params | q if qs_params else q
		# 	qs = qs.filter(qs_params)
		# return qs

	
# VISTAS PARA ADMIN MATRIMONIO

# class MatrimonioCreateView(CreateView):
# 	model=Matrimonio
# 	form_class=MatrimonioForm
# 	template_name='matrimonio/matrimonio_form.html'
# 	success_url='/matrimonio/'

def matrimonio_create_view(request):
	usuario=request.user
	
	if(request.method=='POST'):
		novio = PerfilUsuario.objects.padre()
		novia = PerfilUsuario.objects.madre()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_matrimonio=MatrimonioForm(usuario,novio,novia,celebrante,request.POST)
		if(form_matrimonio.is_valid()):
			matrimonio=form_matrimonio.save(commit=False)
			matrimonio.tipo_sacramento='Matrimonio'
			novio=matrimonio.novio
			novia=matrimonio.novia
			if  (novio.estado_civil!='c') and (novia.estado_civil!='c'):
							
				if (novio.sexo=='m' and novia.sexo=='f'):
					novio.estado_civil='c'
					novia.estado_civil='c'
					novio.save()
					novia.save()
					matrimonio.novio=novio
					matrimonio.novia=novia
					asignacion = AsignacionParroquia.objects.get(
							persona__user=request.user)
					matrimonio.parroquia = asignacion.parroquia
					matrimonio.vigente=True
					matrimonio.save()
					LogEntry.objects.log_action(
						user_id=request.user.id,
	            		content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
	            		object_id=matrimonio.id,
	            		object_repr=unicode(matrimonio),
	            		action_flag=ADDITION,
	            		change_message='Se creo matrimonio')
					messages.success(request,'Creado exitosamente')
					return HttpResponseRedirect('/matrimonio')
				else:
					messages.info(request,'No se puen casar novios con el mismo sexo')
			else:
				messages.info(request,'Uno de los novios ya esta casado')
				
		else:
			novio = request.POST.get('novio')
			novia = request.POST.get('novia')
			celebrante =  request.POST.get('celebrante')
			print(novio)
			print(novia)
			print(celebrante)

			if novio and novia and celebrante:
			    novio = PerfilUsuario.objects.filter(id=novio)
			    novia = PerfilUsuario.objects.filter(id=novia)
			    celebrante = PerfilUsuario.objects.filter(id=celebrante)
			    form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif novio and novia and not celebrante:
				novio = PerfilUsuario.objects.filter(id=novio)
				novia = PerfilUsuario.objects.filter(id=novia)
				celebrante = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif not novio and novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novio= PerfilUsuario.objects.none()
				novia = PerfilUsuario.objects.filter(id=novia)
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif novio and not novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.filter(id=novio)
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif novio and not novia and not celebrante:
				celebrante = PerfilUsuario.objects.none()
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.filter(id=novio)
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif not novio and novia and not celebrante:
				celebrante = PerfilUsuario.objects.none()
				novia= PerfilUsuario.objects.filter(id=novia)
				novio = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)	
			elif not novio and not novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			else:
				novio = PerfilUsuario.objects.none()
				novia = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio,novia, celebrante, request.POST)

			messages.error(request,'Uno o mas campos son invalidos')
			ctx={'form_matrimonio':form_matrimonio}
			return render(request,'matrimonio/matrimonio_form.html',ctx)
		
	else:

		form_matrimonio=MatrimonioForm(usuario)
		
	ctx={'form_matrimonio':form_matrimonio}
	return render(request,'matrimonio/matrimonio_form.html',ctx)


# class MatrimonioUpdateView(UpdateView):
# 	model=Matrimonio
# 	template_name='matrimonio/matrimonio_form.html'
# 	success_url='/matrimonio/'

def matrimonio_update_view(request,pk):
	usuario=request.user
	matrimonio=get_object_or_404(Matrimonio,pk=pk)
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	
	if request.method == 'POST':
		novio = PerfilUsuario.objects.padre()
		novia = PerfilUsuario.objects.madre()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_matrimonio = MatrimonioFormEditar(usuario,novio,novia,celebrante,request.POST,
			instance=matrimonio)
		if form_matrimonio.is_valid():
			matrimonio=form_matrimonio.save(commit=False)
			novio=matrimonio.novio
			novia=matrimonio.novia
			if (novio.sexo=='m' and novia.sexo=='f'):
				novio.estado_civil='c'
				novia.estado_civil='c'
				novio.save()
				novia.save()
				matrimonio.novio=novio
				matrimonio.novia=novia
				asignacion = AsignacionParroquia.objects.get(
						persona__user=request.user)
				matrimonio.parroquia = asignacion.parroquia
				matrimonio.vigente=True
				matrimonio.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
	            	content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
	            	object_id=matrimonio.id,
	            	object_repr=unicode(matrimonio),
	            	action_flag=CHANGE,
	            	change_message='Se actualizo matrimonio')
				messages.success(request,'Actualizado exitosamente')
				return HttpResponseRedirect('/matrimonio')
			else:
				messages.info(request,'No se puen casar novios con el mismo sexo')
			
		else:
			novio = request.POST.get('novio')
			novia = request.POST.get('novia')
			celebrante =  request.POST.get('celebrante')

			if novio and novia and celebrante:
				novio = PerfilUsuario.objects.filter(id=novio)
				novia = PerfilUsuario.objects.filter(id=novia)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
					instance=matrimonio)
			elif novio and novia and not celebrante:
				novio = PerfilUsuario.objects.filter(id=novio)
				novia = PerfilUsuario.objects.filter(id=novia)
				celebrante = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
					instance=matrimonio)
			elif not novio and novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novio= PerfilUsuario.objects.none()
				novia = PerfilUsuario.objects.filter(id=novia)
				form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
					instance=matrimonio)
			elif novio and not novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.filter(id=novio)
				form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
					instance=matrimonio)
			elif novio and not novia and not celebrante:
				celebrante = PerfilUsuario.objects.none()
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.filter(id=novio)
				form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
					instance=matrimonio)

			else:
				novio = PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioFormEditar(usuario,novio,novia, celebrante, request.POST,
					instance=matrimonio)
			print('Error de Actua')
			messages.error(request, 'Uno o mas campos son invalidos')
			ctx = {'form_matrimonio': form_matrimonio,'notas':notas,'object':matrimonio}
			return render(request,'matrimonio/matrimonio_form.html', ctx)
			
	else:
		if matrimonio.novio and matrimonio.novia and matrimonio.celebrante:
			novio = PerfilUsuario.objects.filter(user__id=matrimonio.novio.user.id)
			novia = PerfilUsuario.objects.filter(user__id=matrimonio.novia.user.id)
			celebrante = PerfilUsuario.objects.filter(user__id=matrimonio.celebrante.user.id)
			form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, instance=matrimonio)
										
	ctx = {'form_matrimonio': form_matrimonio,'notas':notas,'object':matrimonio}
	return render(request, 'matrimonio/matrimonio_form.html', ctx)


def matrimonio_vigencia_view(request,pk):
	usuario = request.user
	matrimonio=Matrimonio.objects.get(pk=pk)	
	if request.method == 'POST':
		novio=matrimonio.novio
		novia=matrimonio.novia
		novio.estado_civil='v'
		novia.estado_civil='v'
		novio.save()
		novia.save()
		matrimonio.vigente=False
		matrimonio.save()
		LogEntry.objects.log_action(
			user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
            object_id=matrimonio.id,
            object_repr=unicode(matrimonio),
            action_flag=DELETION,
            change_message='Quitó vigencia del matrimonio')
		messages.success(usuario, 'Se ha quitado la vigencia con exito')
		return HttpResponseRedirect('/matrimonio')

	else:
		form = MatrimonioForm(usuario,instance=matrimonio)
		matrimonio.vigente=False
		matrimonio.save()
	
	ctx = {'form': form}
	return render(request,'matrimonio/matrimonio_list.html', ctx)


def matrimonio_ajax_view(request):
	exito = False
	matrimonio=Matrimonio.objects.all()
	list_matrimonios= list()
	for m in matrimonio:
		novio=u'%s' % m.novio.user.get_full_name()
		novia=u'%s' % m.novia.user.get_full_name()
		list_matrimonios.append({ 'id': m.pk, 'novio':novio,'novia':novia})
	ctx={'list_matrimonios':list_matrimonios, 'exito':exito}
	return HttpResponse(json.dumps(ctx), content_type='application/json')

class MatrimonioNoVigenteListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(
				persona__user=self.request.user)
			queryset = Matrimonio.objects.filter(parroquia=asignacion.parroquia,vigente=False)
			return queryset
		except: 
			return [];


class MatrimonioListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(
				persona__user=self.request.user)

			queryset = Matrimonio.objects.filter(parroquia=asignacion.parroquia,vigente=True)
			return queryset
		except: 
			return [];




# VISTAS PARA ADMIN DE BAUTISMO

def bautismo_create_view(request):
	usuario=request.user
	if(request.method == 'POST' ):
		bautizado=PerfilUsuario.objects.feligres()
		celebrante=PerfilUsuario.objects.sacerdote()
		formBautismo=BautismoForm(usuario,bautizado,celebrante,request.POST)

		# form_nota=NotaMarginalForm(request.POST)
		if (formBautismo.is_valid()):
			#perfil=formPerfil.save(commit=False)
			bautismo=formBautismo.save(commit=False)
			# nota=form_nota.save(commit=False)
			bautismo.tipo_sacramento =  u'Bautismo'
			# nota.save()
			# bautismo.nota_marginal=nota
			asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user)
			bautismo.parroquia = asignacion.parroquia
			bautismo.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(bautismo).pk,
            	object_id=bautismo.id,
            	object_repr=unicode(bautismo),
            	action_flag=ADDITION,
            	change_message='Se creo bautismo')
			
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/bautismo')
		else:
			bautizado = request.POST.get('bautizado')
			celebrante =  request.POST.get('celebrante')

			if bautizado and celebrante:
				bautizado = PerfilUsuario.objects.filter(id=bautizado)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)
			elif bautizado and not celebrante:
				bautizado = PerfilUsuario.objects.filter(id=bautizado)
				celebrante = PerfilUsuario.objects.none()
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)
			elif not bautizado and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				bautizado= PerfilUsuario.objects.none()
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)

			else:
				bautizado = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)

			
			messages.error(request,'Uno o mas campos son invalidos')
			ctx={'formBautismo':formBautismo}
			return render (request,'bautismo/bautismo_form.html',ctx)
	else:
		
		formBautismo=BautismoForm(usuario)
		# form_nota=NotaMarginalForm()
	ctx={'formBautismo':formBautismo}
	return render (request,'bautismo/bautismo_form.html',ctx)


def mostrar():

	return self.model.objects.filter()

# class BautismoCreateView(CreateView):
# 	model=Bautismo
# 	template_name='bautismo/bautismo_form.html'
# 	form_class=BautismoForm
# 	success_url='/bautismo/'



def bautismo_update_view(request,pk):
	usuario=request.user
	bautismo= get_object_or_404(Bautismo, pk=pk)
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	
	if request.method == 'POST':
		bautizado = PerfilUsuario.objects.all()
		celebrante=PerfilUsuario.objects.sacerdote()
		bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante,request.POST,instance=bautismo)
		# form_nota=NotaMarginalForm(request.POST,instance=nota)
		if bautismo_form.is_valid():
			bautismo_form.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(bautismo).pk,
            	object_id=bautismo.id,
            	object_repr=unicode(bautismo),
            	action_flag=CHANGE,
            	change_message='Se Modifico bautismo')
			messages.success(request,'Actualizado exitosamente')
			return HttpResponseRedirect('/bautismo')
		else:
			bautizado = request.POST.get('bautizado')
			celebrante = request.POST.get('celebrante')
			if bautizado and celebrante:
				bautizado = PerfilUsuario.objects.filter(id=bautizado)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, request.POST,
					instance=bautismo)
			elif(bautizado and not celebrante):
				bautizado = PerfilUsuario.objects.filter(id=bautizado)
				celebrante=PerfilUsuario.objects.none()
				bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, request.POST,
					instance=bautismo)
			elif(celebrante and not bautizado):
				bautizado=PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, request.POST,
					instance=bautismo)
		
			else:
				celebrante = PerfilUsuario.objects.none()
				bautizado = PerfilUsuario.objects.none()
				bautismo_form = BautismoFormEditar(usuario, bautizado,celebrante,request.POST, 
					instance=bautismo)

			
			messages.error(request, "Uno o mas campos son invalidos")
			ctx = {'formBautismo': bautismo_form,'notas':notas,'object':bautismo}
			return render(request, 'bautismo/bautismo_form.html', ctx)
			
	else:

		if bautismo.bautizado and bautismo.celebrante:

			bautizado = PerfilUsuario.objects.filter(user__id=bautismo.bautizado.user.id)
			celebrante=PerfilUsuario.objects.filter(user__id=bautismo.celebrante.user.id)
			bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, instance=bautismo)
		else:
			bautismo_form = BautismoFormEditar(instance=bautismo)

		# bautismo_form = BautismoFormEditar(usuario,bautizado,instance=bautismo)
		
		# form_nota=NotaMarginalForm(instance=nota)
									
		ctx = {'formBautismo': bautismo_form,'notas':notas,'object':bautismo}
		return render(request, 'bautismo/bautismo_form.html', ctx)



# class BautismoUpdateView(UpdateView):
# 	model=Bautismo
# 	template_name='bautismo/bautismo_form.html'
# 	success_url= '/bautismo/'

class BautismoListView(ListView):
	model=Bautismo
	template_name='bautismo/bautismo_list.html'
	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user)
			queryset = Bautismo.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];


# VISTAS PARA ADMIN DE EUCARISTIA

# class EucaristiaCreateView(CreateView):
# 	model=Eucaristia
# 	template_name='eucaristia/eucaristia_form.html'
# 	success_url='/eucaristia/'


def eucaristia_create_view(request):
	usuario=request.user
	if request.method == 'POST':
		feligres=PerfilUsuario.objects.feligres()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_eucaristia=EucaristiaForm(usuario,feligres,celebrante,request.POST)
		if form_eucaristia.is_valid():
			eucaristia=form_eucaristia.save(commit=False)
			tipo_sacramento=u'Eucaristia'
			eucaristia.tipo_sacramento=tipo_sacramento
			asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user)
			eucaristia.parroquia = asignacion.parroquia
			eucaristia.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
            	object_id=eucaristia.id,
            	object_repr=unicode(eucaristia),
            	action_flag=ADDITION,
            	change_message='Se creo eucaristia')
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/eucaristia')
		else:
			feligres = request.POST.get('feligres')
			celebrante =  request.POST.get('celebrante')

			if feligres and celebrante:
				feligres = PerfilUsuario.objects.filter(id=feligres)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)
			elif feligres and not celebrante:
				feligres = PerfilUsuario.objects.filter(id=feligres)
				celebrante = PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)
			elif not feligres and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				feligres= PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)

			else:
				feligres = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)
			messages.error(request,"Uno o mas campos son invalidos")
			ctx={'form_eucaristia':form_eucaristia}
			return render(request,'eucaristia/eucaristia_form.html',ctx)
	else:
		form_eucaristia=EucaristiaForm(usuario)

	ctx={'form_eucaristia':form_eucaristia}
	return render(request,'eucaristia/eucaristia_form.html',ctx)


# class EucaristiaUpdateView(UpdateView):
# 	model=Eucaristia
# 	template_name='eucaristia/eucaristia_form.html'
# 	success_url='/eucaristia/'

def eucaristia_update_view(request,pk):
	usuario=request.user
	eucaristia=get_object_or_404(Eucaristia,pk=pk)
	if(request.method == 'POST'):
		feligres= PerfilUsuario.objects.feligres()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_eucaristia=EucaristiaFormEditar(usuario,feligres,celebrante,request.POST,instance=eucaristia)
		if(form_eucaristia.is_valid()):
			form_eucaristia.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
            	object_id=eucaristia.id,
            	object_repr=unicode(eucaristia),
            	action_flag=CHANGE,
            	change_message='Se modifico eucaristia')
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/eucaristia')
		else:

			feligres = request.POST.get('feligres')
			celebrante = request.POST.get('celebrante')
			if feligres and celebrante:
				feligres = PerfilUsuario.objects.filter(id=feligres)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_eucaristia = EucaristiaFormEditar(usuario,feligres,celebrante, request.POST,
					instance=eucaristia)
			elif(feligres and not celebrante):
				feligres = PerfilUsuario.objects.filter(id=feligres)
				celebrante=PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaFormEditar(usuario,feligres, celebrante,request.POST,
					instance=eucaristia)
			elif(celebrante and not feligres):
				feligres=PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_eucaristia = EucaristiaFormEditar(usuario,feligres,celebrante, request.POST,
					instance=eucaristia)
		
			else:
				celebrante = PerfilUsuario.objects.none()
				feligres = PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaFormEditar(usuario, feligres,celebrante,request.POST, 
					instance=eucaristia)

			messages.error(request,"Uno o mas campos son invalidos")
			ctx={'form_eucaristia':form_eucaristia, 'object':eucaristia}
			return render(request,'eucaristia/eucaristia_form.html',ctx)
		
	else:
		if eucaristia.feligres and eucaristia.celebrante:
			feligres = PerfilUsuario.objects.filter(user__id=eucaristia.feligres.user.id)
			celebrante=PerfilUsuario.objects.filter(user__id=eucaristia.celebrante.user.id)
			form_eucaristia = EucaristiaFormEditar(usuario,feligres,celebrante, instance=eucaristia)
		

				
		# form_eucaristia=EucaristiaFormEditar(usuario,feligres,instance=eucaristia)
	ctx={'form_eucaristia':form_eucaristia, 'object':eucaristia}
	return render(request,'eucaristia/eucaristia_form.html',ctx)



class EucaristiaListView(ListView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_list.html'
	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user)
			queryset = Eucaristia.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];

# VISTAS PARA ADMIN DE CONFIRMACION

# class ConfirmacionCreateView(CreateView):
# 	model=Confirmacion
# 	template_name='confirmacion/confirmacion_form.html'
# 	success_url='/confirmacion/'

def confirmacion_create_view(request):
	usuario=request.user
	confirmado=PerfilUsuario.objects.feligres()
	celebrante=PerfilUsuario.objects.sacerdote()
	if(request.method == 'POST'):
		form_confirmacion=ConfirmacionForm(usuario,confirmado,celebrante,request.POST)
		if(form_confirmacion.is_valid()):
			confirmacion=form_confirmacion.save(commit=False)
			confirmacion.tipo_sacramento='Confirmacion'
			asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user)
			confirmacion.parroquia = asignacion.parroquia
			confirmacion.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
            	object_id=confirmacion.id,
            	object_repr=unicode(confirmacion),
            	action_flag=ADDITION,
            	change_message='Se creo confirmacion')
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/confirmacion')
		else:
			confirmado = request.POST.get('confirmado')
			celebrante =  request.POST.get('celebrante')

			if confirmado and celebrante:
				confirmado = PerfilUsuario.objects.filter(id=confirmado)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_confirmacion = ConfirmacionForm(usuario,confirmado, celebrante, request.POST)
			elif confirmado and not celebrante:
				confirmado = PerfilUsuario.objects.filter(id=confirmado)
				celebrante = PerfilUsuario.objects.none()
				form_confirmacion = EucaristiaForm(usuario,confirmado, celebrante, request.POST)
			elif not confirmado and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				confirmado= PerfilUsuario.objects.none()
				form_confirmacion = EucaristiaForm(usuario,confirmado, celebrante, request.POST)

			else:
				confirmado = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_confirmacion = EucaristiaForm(usuario,confirmado, celebrante, request.POST)

			messages.error(request,"Uno o mas campos son invalidos")
			ctx={'form_confirmacion':form_confirmacion}
			return render(request,'confirmacion/confirmacion_form.html',ctx)
			
	else:
		form_confirmacion=ConfirmacionForm(usuario)
	ctx={'form_confirmacion':form_confirmacion}
	return render(request,'confirmacion/confirmacion_form.html',ctx)




# class ConfirmacionUpdateView(UpdateView):
# 	model=Confirmacion
# 	template_name='confirmacion/confirmacion_form.html'
# 	success_url='/confirmacion/'

def confirmacion_update_view(request,pk):
	usuario=request.user
	confirmacion=get_object_or_404(Confirmacion,pk=pk)
	
	if(request.method == 'POST'):
		confirmado=PerfilUsuario.objects.feligres()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_confirmacion=ConfirmacionFormEditar(usuario,confirmado,celebrante,request.POST,
			instance=confirmacion)
		if(form_confirmacion.is_valid()):
			form_confirmacion.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
            	object_id=confirmacion.id,
            	object_repr=unicode(confirmacion),
            	action_flag=CHANGE,
            	change_message='Se modifico confirmacion')
			messages.success(request,'Actualizado exitosamente')
			return HttpResponseRedirect('/confirmacion')
		else:
			confirmado = request.POST.get('confirmado')
			celebrante = request.POST.get('celebrante')
			if confirmado and celebrante:
				confirmado = PerfilUsuario.objects.filter(id=confirmado)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, request.POST,
					instance=confirmacion)
			elif(confirmado and not celebrante):
				confirmado = PerfilUsuario.objects.filter(id=confirmado)
				celebrante=PerfilUsuario.objects.none()
				form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, request.POST,
					instance=confirmacion)
			elif(celebrante and not confirmado):
				confirmado=PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, request.POST,
					instance=confirmacion)
		
			else:
				celebrante = PerfilUsuario.objects.none()
				confirmado = PerfilUsuario.objects.none()
				form_confirmacion = ConfirmacionFormEditar(usuario, confirmado,celebrante,request.POST, 
					instance=confirmacion)
			

			messages.error(request,"Uno o mas campos son invalidos")
			ctx={'form_confirmacion':form_confirmacion,'object':confirmacion}
			return render(request,'confirmacion/confirmacion_form.html',ctx)
	else:
		if confirmacion.confirmado and confirmacion.celebrante:
			confirmado = PerfilUsuario.objects.filter(user__id=confirmacion.confirmado.user.id)
			celebrante = PerfilUsuario.objects.filter(user__id=confirmacion.celebrante.user.id)
			form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, instance=confirmacion)
		else:
			form_confirmacion = EucaristiaFormEditar(instance=confirmacion)

		
	ctx={'form_confirmacion':form_confirmacion,'object':confirmacion}
	return render(request,'confirmacion/confirmacion_form.html',ctx)


class ConfirmacionListView(ListView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user)
			queryset = Confirmacion.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];



#Vistas para crear una parroquia
@login_required(login_url='/login/')
def parroquia_create_view(request):
	template_name = 'parroquia/parroquia_form.html'
	success_url = '/parroquia/'
	if request.method== 'POST':
		form_parroquia = ParroquiaForm(request.POST)
		canton = Canton.objects.all()
		parroquia_civil = ParroquiaCivil.objects.all()
		form_direccion = DireccionForm(canton, parroquia_civil, request.POST)
		if form_parroquia.is_valid() and form_direccion.is_valid():
			parroquia = form_parroquia.save(commit=False)
			direccion = form_direccion.save()
			parroquia.direccion = direccion
			parroquia.save()
			return HttpResponseRedirect(success_url)
		else:
			ctx = {'form_parroquia': form_parroquia, 'form_direccion':form_direccion}
			messages.info(request, ctx)
			messages.info(request, 'errores')
			return render(request, template_name, ctx)
	else:
		form_parroquia = ParroquiaForm()
		form_direccion = DireccionForm()
		ctx = {'form_parroquia': form_parroquia, 'form_direccion':form_direccion}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
def parroquia_update_view(request, pk):
	template_name = 'parroquia/parroquia_form.html'
	success_url = '/parroquia/'
	parroquia = get_object_or_404(Parroquia, pk = pk)
	direccion = parroquia.direccion
	
	if request.method == 'POST':
		form_parroquia = ParroquiaForm(request.POST, instance=parroquia)
		canton = Canton.objects.all()
		parroquia_civil = ParroquiaCivil.objects.all()
		form_direccion = DireccionForm(canton, parroquia_civil, request.POST, instance=direccion)
		if form_parroquia.is_valid() and form_direccion.is_valid():
			form_parroquia.save()
			form_direccion.save()
			# parroquia = form_parroquia.save(commit=False)
			# direccion = form_direccion.save()
			# parroquia.direccion = direccion
			# parroquia.save()
			return HttpResponseRedirect(success_url)
		else:
			ctx = {'form_parroquia':form_parroquia, 'form_direccion':form_direccion}
			messages.info(request, ctx)
			return render(request, template_name, ctx)
	else:
		canton = Canton.objects.filter(provincia=parroquia.direccion.provincia)
		parroquia_civil = ParroquiaCivil.objects.filter(canton=canton)
		form_parroquia = ParroquiaForm(instance=parroquia)
		form_direccion = DireccionForm(instance=direccion, canton = canton, parroquia=parroquia_civil)
		ctx = {'form_parroquia': form_parroquia, 'form_direccion':form_direccion}
		return render(request, template_name, ctx)

class ParroquiaListView(ListView):
	model= Parroquia
	template_name = 'parroquia/parroquia_list.html'


@login_required(login_url='/login/')
def intencion_create_view(request):
	template_name = 'intencion/intencion_form.html'
	success_url = '/intencion/'
	if request.method == 'POST':
		form_intencion = IntencionForm(request.POST)
		if form_intencion.is_valid():
			intencion = form_intencion.save(commit=False)
			try:
				asignacion = AsignacionParroquia.objects.get(persona__user=request.user)
				intencion.parroquia = asignacion.parroquia
				intencion.save()
				messages.success(request, 'Creado exitosamente')
				return HttpResponseRedirect(success_url)
			except ObjectDoesNotExist:
				raise Http404
		else:
			messages.error(request, u'Uno o más campos no son incorrectos')
			ctx = {'form': form_intencion}
			return render(request, template_name, ctx)
	else:
		form_intencion = IntencionForm()
		ctx = {'form': form_intencion}
		return render(request, template_name, ctx)

class IntencionListView(ListView):
	model= Intenciones
	template_name = 'intencion/intencion_list.html'

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(IntencionListView, self).dispatch(*args, **kwargs)

class IntencionUpdateView(UpdateView):
	model= Intenciones
	template_name = 'intencion/intencion_form.html'
	form_class = IntencionForm
	success_url = '/intencion/'
	context_object_name = 'form_intencion'

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(IntencionUpdateView, self).dispatch(*args, **kwargs)

@login_required(login_url='/login/')
def asignar_parroquia_create(request):
	template_name = "parroquia/asignar_parroquia_form.html"
	success_url = '/parroquia/'
	parroquia = request.POST.get('parroquia')
	persona = request.POST.get('persona')
	# estado = self.request.POST.get('estado')
	# print persona


	if request.method == 'POST':
		form = AsignarParroquiaForm(request.POST)
		form_periodo = PeriodoAsignacionParroquiaForm(request.POST)
		if form.is_valid() and form_periodo.is_valid():
			
			try: 
				asignacion = AsignacionParroquia.objects.get(persona__id = persona, parroquia__id = parroquia)
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()


				return HttpResponseRedirect(success_url)

			except ObjectDoesNotExist:
				asignacion = form.save()
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()
				return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Uno o más cámpos son inválidos')
			ctx = {'form': form, 'form_periodo': form_periodo}
			# return render(request, template_name, ctx)
	else:
		form_periodo = PeriodoAsignacionParroquiaForm()
		form = AsignarParroquiaForm()
		ctx = {'form': form, 'form_periodo': form_periodo}
	return render(request, template_name, ctx)

def asignar_parroco_a_parroquia(request, pk):
	template_name = "parroquia/asignar_parroquia_form.html"
	success_url = '/parrocos/parroquia/%s/' % (pk)
	parroquia = get_object_or_404(Parroquia, pk=pk)
	persona = request.POST.get('persona')
	print parroquia
	parroquias = Parroquia.objects.filter(id=pk)
	queryset = Parroquia.objects.all()

	
	if request.method == 'POST':
		form = AsignarParroquiaForm(queryset, request.POST)
		form_periodo = PeriodoAsignacionParroquiaForm(request.POST)
		if form.is_valid() and form_periodo.is_valid():
			try: 
				asignacion = AsignacionParroquia.objects.get(persona__id = persona, parroquia__id = parroquia.id)
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()
				return HttpResponseRedirect(success_url)

			except ObjectDoesNotExist:
				asignacion = form.save()
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()
				return HttpResponseRedirect(success_url)

		else:
			form = AsignarParroquiaForm(parroquias, request.POST)
			messages.error(request, 'Uno o más cámpos son inválidos')
			ctx = {'form': form, 'form_periodo': form_periodo}
			return render(request, template_name, ctx)
	else:
		form = AsignarParroquiaForm(parroquias)
		form_periodo = PeriodoAsignacionParroquiaForm()
		ctx = {'form': form, 'form_periodo': form_periodo, 'object': parroquia}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
def asignar_parroquia_update(request, pk):
	template_name = "parroquia/asignar_parroquia_form.html"
	success_url = '/asignar/parroquia/'
	asignacion = get_object_or_404(AsignacionParroquia, pk=pk)
	periodos = PeriodoAsignacionParroquia.objects.filter(asignacion__id=asignacion.id)

	if request.method == 'POST':
		persona = PerfilUsuario.objects.feligres()
		form = AsignarParroquiaForm(request.POST, instance=asignacion)
		form_periodo = periodos
		if form.is_valid() and form_periodo.is_valid():
			asignacion = form.save(commit=False)
			periodo = form_periodo.save()
			asignacion.periodo = periodo
			form.save()
			return HttpResponseRedirect(success_url)
		else:
			messages.error(request, 'Uno o más cámpos son inválidos')
			ctx = {'form': form, 'form_periodo': form_periodo, 'object': asignacion.parroquia}
			# return render(request, template_name, ctx)
	else:
		form_periodo = periodos
		form = AsignarParroquiaForm(instance=asignacion)
		ctx = {'form': form, 'form_periodo': form_periodo, 'object': asignacion.parroquia}
	return render(request, template_name, ctx)

def nuevo_periodo_asignacion(request, pk):
	template_name = 'parroquia/periodo_asignacion_form.html'
	asignacion = AsignacionParroquia.objects.get(id=pk)
	success_url = '/parroco/periodos/asignacion/%s/' % asignacion.id
	if request.method == 'POST':
		form = PeriodoAsignacionParroquiaForm(request.POST)
		if form.is_valid():
			periodo_activo= PeriodoAsignacionParroquia.objects.filter(asignacion=asignacion, estado=True)
			
			if not periodo_activo:
				periodo = form.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				return HttpResponseRedirect(success_url)
			else:
				messages.error(request, 'Existen periodos activos')
				ctx = {'form': form, 'object':asignacion}
				return render(request, template_name, ctx)

		else:
			ctx = {'form': form, 'object':asignacion}
			return render(request, template_name, ctx)

	else:
		form = PeriodoAsignacionParroquiaForm()
		ctx = {'form': form, 'object':asignacion}
		return render(request, template_name, ctx)

def parroco_periodos_asignacion_update(request, pk):
	periodo = get_object_or_404(PeriodoAsignacionParroquia, pk = pk)
	template_name = 'parroquia/periodo_asignacion_form.html'
	success_url = u'/parroco/periodos/asignacion/%s/' % periodo.asignacion.id

	if request.method == 'POST':
		estado = request.POST.get('estado')
		form = PeriodoAsignacionParroquiaForm(request.POST, instance=periodo)
		periodo_activo= PeriodoAsignacionParroquia.objects.filter(asignacion=periodo.asignacion, estado=True).exclude(id=periodo.id)
		if form.is_valid():
			
			if not periodo_activo:

				if estado:
					user = PerfilUsuario.objects.get(pk=periodo.asignacion.persona.id).user
					user.is_staff = True
					user.save()
				else: 
					user = PerfilUsuario.objects.get(pk=periodo.asignacion.persona.id).user
					user.is_staff = False
					user.save()
				form.save() 
				return HttpResponseRedirect(success_url)
			else:
				messages.error(request, 'Existen periodos activos')
				ctx = {'form': form, 'object':periodo.asignacion}
				return render(request, template_name, ctx)
		else:
			ctx = {'form': form, 'object':periodo.asignacion}
			return render(request, template_name, ctx)

	else:
		form = PeriodoAsignacionParroquiaForm(instance=periodo)
		ctx = {'form': form, 'object':periodo.asignacion}
		return render(request, template_name, ctx)


# El pk que recibe es el id de una asignación
@login_required(login_url='/login/')
def parroco_periodos_asignacion_list(request, pk):
	template_name = "parroquia/parroco_periodos_asignacion_list.html"
	success_url = '/asignar/parroquia/'
	# parroquia = get_object_or_404(Parroquia, pk=pk)
	periodos = PeriodoAsignacionParroquia.objects.filter(asignacion__id=pk)
	asignacion = get_object_or_404(AsignacionParroquia, pk=pk)
	ctx = {'object_list': periodos, 'asignacion': asignacion}
	return render(request, template_name, ctx)

def asignar_parroco_list(request, pk):
	template_name = 'parroquia/asignar_parroquia_list.html'
	object_list = AsignacionParroquia.objects.filter(parroquia__id=pk).exclude(periodoasignacionparroquia=None)
	parroquia = get_object_or_404(Parroquia, pk=pk)
	ctx = {'object_list': object_list, 'parroquia':parroquia}
	return render(request, template_name, ctx)
	


class AsignarParroquiaCreate(CreateView):
	model = AsignacionParroquia
	form_class = AsignarParroquiaForm
	template_name = 'parroquia/asignar_parroquia_form.html'
	success_url = '/asignar/parroquia/'
	

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(AsignarParroquiaCreate, self).dispatch(*args, **kwargs)


	def form_valid(self, form):
		persona_id = self.request.POST['persona']
		estado = self.request.POST.get('estado')
		if estado:
			user = PerfilUsuario.objects.get(pk=persona_id).user
			user.is_staff = True 
			user.save()
		
		return super(AsignarParroquiaCreate, self).form_valid(form)


class AsignarParroquiaUpdate(UpdateView):
	model = AsignacionParroquia
	form_class = AsignarParroquiaForm
	template_name = 'parroquia/asignar_parroquia_form.html'
	success_url = '/asignar/parroquia/'	

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(AsignarParroquiaUpdate, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		persona_id = self.request.POST['persona']
		estado = self.request.POST.get('estado')
		if estado:
			user = PerfilUsuario.objects.get(pk=persona_id).user
			user.is_staff = True 
			user.save()
		else:
			user = PerfilUsuario.objects.get(pk=persona_id).user
			user.is_staff = False
			user.save()
		
		return super(AsignarParroquiaUpdate, self).form_valid(form)


class AsignarParroquiaList(ListView):
	model = AsignacionParroquia
	template_name = 'parroquia/asignar_parroquia_list.html'

	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(AsignarParroquiaList, self).dispatch(*args, **kwargs)


@login_required
def asignar_secretaria_create(request):
	template_name = "parroquia/asignar_secretaria_form.html"
	success_url = '/asignar/secretaria/'
	usuario = request.user
	if request.method == 'POST':
		persona = PerfilUsuario.objects.feligres()
		form = AsignarSecretariaForm(usuario, persona, request.POST.get('estado'), request.POST)
		if form.is_valid():
			try:
				asignacion = AsignacionParroquia.objects.get(persona=request.POST.get('persona'))
				messages.error(request, 'El usuario ya se encuentra asignado')
				ctx = {'form': form}
				return render(request, template_name, ctx)
			except ObjectDoesNotExist:
				form.save()
				persona_id = request.POST['persona']
				estado = request.POST.get('estado')
				if estado:
					user = PerfilUsuario.objects.get(pk=persona_id).user
					user.is_staff = True 
					user.save()
				else:
					user = PerfilUsuario.objects.get(pk=persona_id).user
					user.is_staff = False
					user.save()
				return HttpResponseRedirect(success_url)
		else:
			messages.error(request, 'Uno o más cámpos son inválidos')
			if request.POST.get('persona'):
				personas = PerfilUsuario.objects.filter(id=request.POST.get('persona'))
				form = AsignarSecretariaForm(usuario, personas, request.POST.get('estado'), request.POST)
				ctx = {'form': form}
				
			else: 
				persona = PerfilUsuario.objects.none()
				form = AsignarSecretariaForm(usuario, persona, request.POST.get('estado'), request.POST)
				ctx = {'form': form}
			return render(request, template_name, ctx)
			
	else:
		form = AsignarSecretariaForm(usuario)
		ctx = {'form': form}
	return render(request, template_name, ctx)

@login_required
def asignar_secretaria_update(request, pk):
	asignacion = get_object_or_404(AsignacionParroquia, pk=pk)
	template_name = "parroquia/asignar_secretaria_form.html"
	success_url = '/asignar/secretaria/'
	usuario = request.user
	if request.method == 'POST':
		persona = PerfilUsuario.objects.feligres()
		form = AsignarSecretariaForm(usuario, persona, asignacion.persona.user.is_staff, request.POST, instance=asignacion)
		if form.is_valid():
			persona_id = request.POST['persona']
			estado = request.POST.get('estado')
			if estado:
				user = PerfilUsuario.objects.get(pk=persona_id).user
				user.is_staff = True 
				user.save()
			else:
				user = PerfilUsuario.objects.get(pk=persona_id).user
				user.is_staff = False
				user.save()
			form.save()
			return HttpResponseRedirect(success_url)
		else:
			if asignacion.persona:
				messages.error(request, '1.- Uno o más cámpos son inválidos %s' % form) 
				persona = PerfilUsuario.objects.filter(user__id=asignacion.persona.user.id)
				form = AsignarSecretariaForm(usuario, persona, asignacion.persona.user.is_staff, request.POST, instance=asignacion)
			else:
				messages.error(request, '2.- Uno o más cámpos son inválidos %s' % form) 
				persona = PerfilUsuario.objects.none()
				form = AsignarSecretariaForm(usuario, persona, request.POST,  instance=asignacion)

			ctx = {'form': form}
			return render(request, template_name, ctx)
	else:
		if asignacion.persona:
			persona = PerfilUsuario.objects.filter(user__id=asignacion.persona.user.id)
			form = AsignarSecretariaForm(usuario, persona, asignacion.persona.user.is_staff, instance=asignacion)
		else:
			persona = PerfilUsuario.objects.none()
			form = AsignarSecretariaForm(usuario, persona, asignacion.persona.user.is_staff, instance=asignacion)
		
		ctx = {'form': form}
		return render(request, template_name, ctx)

class AsignarSecretariaList(ListView):
	model = AsignacionParroquia
	template_name = 'parroquia/asignar_secretaria_list.html'
	queryset = AsignacionParroquia.objects.exclude(persona__profesion='Sacerdote')	
	
	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(AsignarSecretariaList, self).dispatch(*args, **kwargs)

# views para los LOGS del ekklesia

class LogListView(ListView):
	model=LogEntry
	template_name='log/log_list.html'

	def get_queryset(self):
		try:
			if (self.request.user.is_superuser):

				queryset = LogEntry.objects.all()
				return queryset
			else:
				queryset=LogEntry.objects.filter(user=self.request.user)
				return queryset

		except: 
			return [];
	

# TODOS LOS REPORTES


def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def libro_pdf(request, pk):
	libro=get_object_or_404(Libro, pk=pk)
	html = render_to_string('libro/libro.html', {'pagesize':'A4', 'libro':libro}, 
		context_instance=RequestContext(request))
	return generar_pdf(html)


def matrimonio_certificado(request, pk):
	matrimonio=get_object_or_404(Matrimonio, pk=pk)
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,asignacion=secretaria)
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	html = render_to_string('matrimonio/matrimonio_certificado.html', {'pagesize':'A4', 
		'matrimonio':matrimonio,'cura':cura,'notas':notas,'secretaria':secretaria},
		context_instance=RequestContext(request))
	return generar_pdf(html)

def matrimonio_acta(request, pk):
	matrimonio=get_object_or_404(Matrimonio, pk=pk)
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,estado=True)
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	html = render_to_string('matrimonio/matrimonio_acta.html', {'pagesize':'A4', 
		'matrimonio':matrimonio,'cura':cura,'notas':notas},
		context_instance=RequestContext(request))
	return generar_pdf(html)

def bautismo_certificado(request, pk):
	bautismo=get_object_or_404(Bautismo, pk=pk)
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,estado=True)
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('bautismo/bautismo_certificado.html', {'pagesize':'A4', 'bautismo':bautismo,
		'cura':cura,'notas':notas,'secretaria':secretaria},context_instance=RequestContext(request))
	return generar_pdf(html)

def bautismo_acta(request, pk):
	bautismo=get_object_or_404(Bautismo, pk=pk)
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,estado=True)
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('bautismo/bautismo_acta.html', {'pagesize':'A4', 'bautismo':bautismo,
		'cura':cura,'notas':notas,'secretaria':secretaria},context_instance=RequestContext(request))
	return generar_pdf(html)

def confirmacion_reporte(request, pk):
	confirmacion=get_object_or_404(Confirmacion, pk=pk)
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,estado=True)
	html = render_to_string('confirmacion/confirmacion_certificado.html', 
		{'pagesize':'A4', 'confirmacion':confirmacion,'cura':cura,'secretaria':secretaria},
		context_instance=RequestContext(request))
	return generar_pdf(html)


def eucaristia_reporte(request, pk):
	eucaristia=get_object_or_404(Eucaristia, pk=pk)
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,estado=True)
	# notas=NotaMarginal.objects.filter()
	html = render_to_string('eucaristia/eucaristia_certificado.html', {'pagesize':'A4', 'eucaristia':eucaristia,
		'cura':cura,'secretaria':secretaria},context_instance=RequestContext(request))
	return generar_pdf(html)

def usuario_reporte_honorabilidad(request,pk):
	perfil=get_object_or_404(PerfilUsuario,pk=pk)
	# parroquia=AsignacionParroquia.objects.get(persona__user=request.user).parroquia
	secretaria=AsignacionParroquia.objects.get(persona__user=request.user)
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=secretaria.parroquia,estado=True)
	html = render_to_string('usuario/certificado_honorabilidad.html', {'pagesize':'A4', 'perfil':perfil,
		'cura':cura,'secretaria':secretaria},context_instance=RequestContext(request))
	return generar_pdf(html)

def reporte_anual_sacramentos(request):
	anio_actual=request.GET.get('anio')
	# print("El año ingresado es: %d"%anio_actual)
	template_name = "reportes/reporte_anual_sacramentos_form.html"
	if anio_actual== anio_actual:

		if anio_actual:
			ninios1=0
			ninios7=0
			ninios=0
			parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
			bautismos=Bautismo.objects.filter(fecha_sacramento__year=anio_actual,parroquia=parroquia.parroquia)
			num_bautizos=len(bautismos)
			for b in bautismos:
				print("Bautismos en 2013 son: %s" %(len(bautismos)))
				num_bautizos=len(bautismos)
				anios_bautizados=b.bautizado.fecha_nacimiento.year
				# print('años de los bautizados en año:%d son: %d' %(int(anio_actual),bautizados))
				resta=int(anio_actual)-anios_bautizados
				if(resta<=1):
					ninios1=ninios1+1
					print ("Niños hasta 1 año %s"%ninios1)
				elif(resta>1 and resta<=7):
					ninios7=ninios7+1
					print('Niños de 1 a 7: %s' %ninios7)
				else:
					ninios=ninios+1
					print('Niños mayores de 7: %s' % ninios)

			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=parroquia.parroquia,estado=True)
			# bautismos=Bautismo.objects.filter(fecha_sacramento__year=anio_actual).count()
			eucaristias=Eucaristia.objects.filter(fecha_sacramento__year=anio_actual,
				parroquia=parroquia.parroquia).count()
			confirmaciones=Confirmacion.objects.filter(fecha_sacramento__year=anio_actual,
				parroquia=parroquia.parroquia).count()
			catolicos=Matrimonio.objects.filter(fecha_sacramento__year=anio_actual,
				tipo_matrimonio='Catolico',parroquia=parroquia.parroquia).count()
			mixtos=Matrimonio.objects.filter(fecha_sacramento__year=anio_actual,tipo_matrimonio='Mixto',
				parroquia=parroquia.parroquia).count()
			matrimonios=catolicos+mixtos
			
			form = ReporteSacramentosAnualForm(request.GET)
			if form.is_valid():
				html=render_to_string('reportes/reporte_anual_sacramentos.html',
				{'pagesize':'A4','num_bautizos':num_bautizos,'ninios1':ninios1,'ninios7':ninios7,
				'ninios':ninios,'eucaristias':eucaristias,'confirmaciones':confirmaciones,
				'catolicos':catolicos,'mixtos':mixtos,'parroquia':parroquia,'cura':cura,
				'anio_actual':anio_actual,'matrimonios':matrimonios},
				context_instance=RequestContext(request))
				return generar_pdf(html)
				
				
			else:
				messages.error(request, 'Uno o más cámpos son inválidos %s' % form)
				ctx = {'form': form}
				# return render(request, template_name, ctx)
		else:
			form = ReporteSacramentosAnualForm()
	else:
		messages.error(request, 'El año tiene que ser de 4 digitos')
		ctx = {'form': form}


		
	ctx={'form':form}
	return render(request, template_name, ctx)
	
def reporte_intenciones(request):
	tipo=request.GET.get('tipo')
	fecha=request.GET.get('fecha')
	# mes=request.GET.get('fecha')
	hora=request.GET.get('hora')
	template_name = "reportes/reporte_intenciones_form.html"
	if tipo=='d':
		if fecha and not hora:

			parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
			intenciones=Intenciones.objects.filter(fecha=fecha,
				parroquia=parroquia.parroquia).order_by('hora')
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=parroquia.parroquia,estado=True)
			form = ReporteIntencionesForm(request.GET)
			if form.is_valid():
				html=render_to_string('reportes/reporte_intenciones.html',
				{'pagesize':'A4','intenciones':intenciones,'parroquia':parroquia,'cura':cura},
				context_instance=RequestContext(request))
				return generar_pdf(html)
			
			
			else:
				messages.error(request, 'Uno o más cámpos son inválidos %s' % form)
				ctx = {'form': form}
			# return render(request, template_name, ctx)

		if fecha and hora:
			parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
			intenciones=Intenciones.objects.filter(fecha=fecha,hora=hora,
				parroquia=parroquia.parroquia).order_by('hora')
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=parroquia.parroquia,estado=True)
			form = ReporteIntencionesForm(request.GET)
			if form.is_valid():
				html=render_to_string('reportes/reporte_intenciones.html',
				{'pagesize':'A4','intenciones':intenciones,'parroquia':parroquia,'cura':cura},
				context_instance=RequestContext(request))
				return generar_pdf(html)
			
			
			else:
				messages.error(request, 'Uno o más cámpos son inválidos %s' % form)
				ctx = {'form': form}

	if tipo=='m':
		
		if fecha :
			mes=fecha[5:7]
			anio=fecha[:4]
			
			parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
			intenciones=Intenciones.objects.filter(fecha__year=anio,fecha__month=mes,
				parroquia=parroquia.parroquia).order_by('hora')
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=parroquia.parroquia,estado=True)
			form = ReporteIntencionesForm(request.GET)
			if form.is_valid():
				html=render_to_string('reportes/reporte_intenciones.html',
				{'pagesize':'A4','intenciones':intenciones,'parroquia':parroquia,'cura':cura},
				context_instance=RequestContext(request))
				return generar_pdf(html)
			
			
			else:
				messages.error(request, 'Uno o más cámpos son inválidos %s' % form)
				ctx = {'form': form}
			# return render(request, template_name, ctx)
	if tipo=='a':
		if fecha:
			fecha=fecha
			anio=fecha[:4]
			print('el año es %s'%int(anio))
			parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
			intenciones=Intenciones.objects.filter(fecha__year=anio,
				parroquia=parroquia.parroquia).order_by('hora')
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=parroquia.parroquia,estado=True)
			form = ReporteIntencionesForm(request.GET)
			if form.is_valid():
				html=render_to_string('reportes/reporte_intenciones.html',
				{'pagesize':'A4','intenciones':intenciones,'parroquia':parroquia,'cura':cura},
				context_instance=RequestContext(request))
				return generar_pdf(html)
			
			
			else:
				messages.error(request, 'Uno o más cámpos son inválidos %s' % form)
				ctx = {'form': form}
	else:
		form = ReporteIntencionesForm()
	
		
	
		
	ctx={'form':form}
	return render(request, template_name, ctx)


def reporte_permisos(request):
	feligres=request.GET.get('feligres')
	tipo=request.GET.get('tipo')
	template_name = "reportes/reporte_permiso_form.html"
	if (tipo =='Bautismo' and feligres):
		
		feligres=PerfilUsuario.objects.get(pk=feligres)
		print(feligres)
		parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
		cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
			parroquia=parroquia.parroquia,estado=True)
		form = ReportePermisoForm(request.GET)
		# if form.is_valid():
		html=render_to_string('reportes/reporte_permiso.html',
		{'pagesize':'A4','feligres':feligres,'parroquia':parroquia,'cura':cura,
		'tipo':tipo},
		context_instance=RequestContext(request))
		return generar_pdf(html)
		
		# else:
			# messages.error(request, 'Uno o más cámpos son inválidos %s' % form.errors)
			# ctx = {'form': form}
	if (tipo =='Eucaristia' and feligres):
		
		
		feligres=PerfilUsuario.objects.get(id=feligres)
		parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
		cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
			parroquia=parroquia.parroquia,estado=True)
		form = ReportePermisoForm(request.GET)
		print('despues del form')
		# if form.is_valid():
		html=render_to_string('reportes/reporte_permiso.html',
		{'pagesize':'A4','feligres':feligres,'parroquia':parroquia,'cura':cura,
		'tipo':tipo},
		context_instance=RequestContext(request))
		print('despues de renderizar el html')
		return generar_pdf(html)
			
			
		# else:
			# messages.error(request, 'Uno o más cámpos son inválidos')
			# ctx = {'form': form}

	if (tipo =='Confirmacion' and feligres):
		
		feligres=PerfilUsuario.objects.get(id=feligres)
		
		parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
		cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
			parroquia=parroquia.parroquia,estado=True)
		form = ReportePermisoForm(request.GET)
		# if form.is_valid():
		html=render_to_string('reportes/reporte_permiso.html',
		{'pagesize':'A4','feligres':feligres,'parroquia':parroquia,'cura':cura,
		'tipo':tipo},
		context_instance=RequestContext(request))
		return generar_pdf(html)
			
			
		# else:
			# messages.error(request, 'Uno o más cámpos son inválidos')
			# ctx = {'form': form}

	if (tipo =='Matrimonio' and feligres):
		
		form = ReportePermisoForm(request.GET)
		feligres=PerfilUsuario.objects.get(id=feligres)
		parroquia= AsignacionParroquia.objects.get(persona__user=request.user)
		cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
			parroquia=parroquia.parroquia,estado=True)
		# if form.is_valid():
		html=render_to_string('reportes/reporte_permiso.html',
		{'pagesize':'A4','feligres':feligres,'parroquia':parroquia,'cura':cura,
		'tipo':tipo},
		context_instance=RequestContext(request))
		return generar_pdf(html)
		
			
		# else:
			# messages.error(request, 'Uno o más cámpos son inválidos')
			# ctx = {'form': form}
	else:
		form = ReportePermisoForm()
	

	ctx={'form':form}
	return render(request, template_name, ctx)

# exportar a csv los logs

def exportar_csv_logs(request):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename="logs.csv"'
    writer = csv.writer(response)
    logs = LogEntry.objects.all()
    writer.writerow(['id','action_time','user_id','content_type','object_id','object_repr','action_flag','change_message']) 
    for log in logs:
    	writer.writerow([log.id,log.action_time,log.user,log.content_type,log.object_id,encode(log.object_repr),log.action_flag,encode(log.change_message)])
    return response

# para poder exportar a csv con utf-8
def encode(text):
	return text.encode('utf-8')

# solo de prueba o modelo no funciona en nada
def report(request):
	tipo=request.GET.get('tipo_sacramento')
	anio=request.GET.get('anio')
	print('Valor de Tipo: %s'%tipo)
	print('Valor de anio: %s'%anio)

	template_name = "reportes/reportes.html"
	# success_url = '/asignar/secretaria/'
	# usuario = request.user
	if tipo and anio:
		bautismos=Bautismo.objects.filter(fecha_sacramento__year=anio)
		form = ReporteForm(request.GET)
		if form.is_valid():
			html = render_to_string('reportes/resultado.html', {'pagesize':'A4','bautismos':bautismos },
				context_instance=RequestContext(request))
			return generar_pdf(html)
			
		else:
			messages.error(request, 'Uno o más cámpos son inválidos %s' % form)
			ctx = {'form': form}
			# return render(request, template_name, ctx)
	else:
		form = ReporteForm()
		
	ctx={'form':form}
	return render(request, template_name, ctx)


