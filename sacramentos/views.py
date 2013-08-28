# -*- coding:utf-8 -*-
# Create your views here.
import json
from datetime import datetime

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
from ho import pisa
import StringIO 
import cgi

from .models import (PerfilUsuario,
	Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,NotaMarginal,
	Parroquia, Intenciones,
	AsignacionParroquia,
	)

from .forms import (
	UsuarioForm, PerfilUsuarioForm, PadreForm,
	MatrimonioForm,MatrimonioFormEditar,
	BautismoForm,BautismoFormEditar,
	EucaristiaForm,EucaristiaFormEditar,
	ConfirmacionForm,ConfirmacionFormEditar,
	LibroForm,NotaMarginalForm,
	DivErrorList,
	IntencionForm,
	ParroquiaForm, 
	SacerdoteForm,
	AsignarParroquiaForm,
	)

from ciudades.forms import DireccionForm
from ciudades.models import Canton, Provincia, Parroquia as ParroquiaCivil



# def usuarioCreateView(request):
# 	if request.is_ajax():
# 		if request.method == 'POST':
# 			valido = False
# 			usuario_form = UsuarioForm(request.POST)
# 			perfil_form = PerfilUsuarioForm(request.POST)
# 			if usuario_form.is_valid() and perfil_form.is_valid():
# 				valido = True
# 				usuario = usuario_form.save(commit=False)
# 				perfil = perfil_form.save(commit=False)
# 				usuario.username = '%s%s%s' %(usuario.first_name, usuario.last_name, perfil.dni)
# 				usuario.save()
# 				perfil.user = usuario
# 				perfil.save()
# 				ctx = {'valido': valido}
				

# 			else:
# 				errores_usuario = usuario_form.errors
# 				errores_perfil =  perfil_form.errors
# 				ctx = {'valido': valido, 'errores_usuario':errores_usuario, 'errores_perfil': errores_perfil}

# 			return HttpResponse(json.dumps(ctx), content_type='application/json')
# 	else:
# 		usuario_form = UsuarioForm()
# 		perfil_form = PerfilUsuarioForm()
# 		ctx = {'usuario_form': usuario_form, 'perfil_form': perfil_form}
# 		return render (request, 'usuario/usuario_form.html', ctx)


def crear_username(username):
	users =  User.objects.filter(username__startswith='admin').order_by('-username')[0]
	# for i
	# valor_original = user_name_original
	# username = user_name
	# try:
	# 	usuario = User.objects.get(username=user_name)
	# 	username = user_name_original + str(i)
	# 	print '%s: %s' % ('Username', username)
	# 	contador = int(i) + int(1)
	# 	print type(contador)
	# 	print u'%s %s' %('Contador: ', contador)
	# 	crear_username(valor_original, username, contador)
	# except:
	# 	return username
	# return username

@login_required
def usuarioCreateView(request):
	if request.method == 'POST':
		valido = False
		form_usuario = UsuarioForm(request.POST)
		form_perfil = PerfilUsuarioForm(request.POST, error_class=DivErrorList)
		if form_usuario.is_valid() and form_perfil.is_valid():
			feligres, created = Group.objects.get_or_create(name='Feligres')
			valido = True
			usuario = form_usuario.save(commit=False)
			perfil = form_perfil.save(commit=False)
			usuario.username = perfil.crear_username(usuario.first_name, usuario.last_name)
			# usuario.username = perfil.dni
			usuario.save()
			usuario.groups.add(feligres)
			perfil.user = usuario
			perfil.save()
			ctx = {'valido': valido}
			return HttpResponseRedirect('/usuario')
			
		else:
			errores_usuario = form_usuario.errors
			errores_perfil =  form_perfil.errors
			messages.info(request, errores_usuario)
			messages.info(request, errores_perfil)
			# ctx = {'valido': valido, 'errores_usuario':errores_usuario, 'errores_perfil': errores_perfil}
			ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil}
			return render (request, 'usuario/usuario_form.html', ctx)
	else:
		form_usuario = UsuarioForm(label_suffix=':', error_class=DivErrorList)
		form_perfil = PerfilUsuarioForm(label_suffix=':')
		# form_perfil.fields['madre'] = forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), required=False, empty_label='--- Seleccione ---')
		# form_perfil.fields['padre'] = forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), required=False, empty_label='--- Seleccione ---')
		ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil}
		return render (request, 'usuario/usuario_form.html', ctx)

def edit_usuario_view(request,pk):
	perfil= get_object_or_404(PerfilUsuario, pk=pk)
	user= perfil.user	
	if request.method == 'POST':
		form_usuario = UsuarioForm(request.POST,instance=user)
		form_perfil = PerfilUsuarioForm(request.POST,instance=perfil)
		if form_usuario.is_valid() and form_perfil.is_valid():
			form_usuario.save()
			form_perfil.save()
			return HttpResponseRedirect('/usuario')
		else:
			messages.info(request, 'Errores al actualizar')
			ctx = {'form_usuario': form_usuario,'form_perfil':form_perfil, 'perfil':perfil}


	else:
		form_usuario = UsuarioForm(instance=user)
		form_perfil = PerfilUsuarioForm(instance=perfil)
									
	ctx = {'form_usuario': form_usuario,'form_perfil':form_perfil, 'perfil':perfil}
	return render(request, 'usuario/usuario_form.html', ctx)

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

def feligres_create_view(request):
	
		if request.method == 'POST':
			usuario_form = UsuarioForm(request.POST)
			perfil_form = PerfilUsuarioForm(request.POST)
			if usuario_form.is_valid() and perfil_form.is_valid():
				pass
		else: 
			usuario_form = UsuarioForm()
			perfil_form = PerfilUsuarioForm()

		ctx = {'usuario_form': usuario_form, 'perfil_form': perfil_form}
		return render(request, 'usuario/feligres.html', ctx) 



class UsuarioListView(ListView):
	model=User
	model=PerfilUsuario
	template_name="usuario/usuario_list.html"



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
			parroquia = AsignacionParroquia.objects.get(
				persona__user=request.user,estado=True).parroquia
			libro.parroquia = parroquia

			try:

				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,parroquia=parroquia)
				if(estado != consulta.estado and tipo!=consulta.tipo_libro):
					if libro.fecha_cierre_mayor():
						libro.save()
						messages.success(request, 'Creado exitosamente')
						return HttpResponseRedirect('/libro')
					else:
						messages.info(request,'La fecha de cierre no puede ser menor'+
						' o igual a fecha de apertura')
						# messages.add_message(request,messages.WARNING,
						# {'Fecha':'La fecha de cierre no puede ser menor o igual a fecha de apertura'})

				elif(estado != consulta.estado and tipo==consulta.tipo_libro):
					if libro.fecha_cierre_mayor():
						libro.save()
						messages.success(request, 'Creado exitosamente')
						return HttpResponseRedirect('/libro')
					else:
						messages.info(request,'La fecha de cierre no puede ser menor'+
						' o igual a fecha de apertura')
						# messages.add_message(request,messages.WARNING,
						# {'Fecha':'La fecha de cierre no puede ser menor o igual a fecha de apertura'})
				else:

					messages.info(request,'Ya existe un libro abierto, cierrelo '+
						'y vuela a crear')
					# messages.add_message(request,messages.WARNING,
					# 	{'Libro':'Ya existe un libro abierto, cierrelo y vuela a crear'})

			except ObjectDoesNotExist:
				libro.save()
				messages.success(request, 'Creado exitosamente')
				return HttpResponseRedirect('/libro')
				

		else:
			messages.error(request,form_libro.errors)
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
	libro=get_object_or_404(Libro,pk=pk)
	if(request.method=='POST'):
		form_libro=LibroForm(request.POST,instance=libro)
		if(form_libro.is_valid()):
			libro=form_libro.save(commit=False)
			estado=libro.estado
			tipo=libro.tipo_libro
			parroquia = AsignacionParroquia.objects.get(
				persona__user=request.user,estado=True).parroquia
			

			try:

				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,
					parroquia=parroquia)
				
				if(estado != consulta.estado and tipo==consulta.tipo_libro):
					if libro.fecha_cierre_mayor():
						libro.parroquia = parroquia
						libro.save()
						return HttpResponseRedirect('/libro')
					else:
						messages.info(request,'La fecha de cierre no puede ser menor'+
						' o igual a fecha de apertura')
				else:
					messages.info(request,'Ya existe un libro abierto, cierrelo '+
						'y vuela a crear')

			except ObjectDoesNotExist:
				libro.parroquia = parroquia
				libro.save()
				messages.success(request, 'Actualizado exitosamente')
				return HttpResponseRedirect('/libro')
				

		else:
			
			messages.error(request,form_libro.errors)
			ctx={'form_libro':form_libro,'object':libro}
			return render(request,'libro/libro_form.html',ctx)
	else:
		form_libro=LibroForm(instance=libro)
	ctx={'form_libro':form_libro,'object':libro}
	return render(request,'libro/libro_form.html',ctx)


class LibroListView(ListView):
	model = Libro
	template_name = 'libro/libro_list.html'

	def get_queryset(self):
		try:
			parroquia = AsignacionParroquia.objects.get(persona__user=self.request.user).parroquia
			queryset = Libro.objects.filter(parroquia=parroquia)
			return queryset
		except: 
			return [];
		# return Libro.objects.filter(numero_libro=12)
		# self.publisher = get_object_or_404(Publisher, name=self.args[0])
		# return Book.objects.filter(publisher=self.publisher)



	# paginate_by = 5
	# def get_queryset(self):
	# 	queryset=super(LibroListView, self).get_queryset()
	# 	query = self.request.GET.get('q')
	# 	if query:
	# 		return queryset.filter(tipo_libro__icontains=query)
	# 	return queryset

	
# VISTAS PARA ADMIN MATRIMONIO

# class MatrimonioCreateView(CreateView):
# 	model=Matrimonio
# 	form_class=MatrimonioForm
# 	template_name='matrimonio/matrimonio_form.html'
# 	success_url='/matrimonio/'

def matrimonio_create_view(request):
	usuario=request.user
	if(request.method=='POST'):
		form_matrimonio=MatrimonioForm(usuario,request.POST)
		if(form_matrimonio.is_valid()):
			matrimonio=form_matrimonio.save(commit=False)
			matrimonio.tipo_sacramento='Matrimonio'
			novio=matrimonio.novio
			novia=matrimonio.novia
			novio.estado_civil='c'
			novia.estado_civil='c'
			novio.save()
			novia.save()
			matrimonio.novio=novio
			matrimonio.novia=novia

			if(matrimonio.novio.estado_civil=='c' and matrimonio.novia.estado_civil=='c'):
				parroquia = AsignacionParroquia.objects.get(
							persona__user=request.user,estado=True).parroquia
				matrimonio.parroquia = parroquia
				matrimonio.save()
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/matrimonio')
			else:
				messages.info(request,'Errores en estado civil')
				
		else:
			messages.error(request,form_matrimonio.errors)
		
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
		form_matrimonio = MatrimonioFormEditar(usuario,request.POST,instance=matrimonio)
		if form_matrimonio.is_valid():
			form_matrimonio.save()
			messages.success(request,'Actualizado exitosamente')
			return HttpResponseRedirect('/matrimonio')
		else:
			messages.error(request, 'Error al actualizar')
			ctx = {'form_matrimonio': form_matrimonio,'notas':notas,'object':matrimonio}
			return render(request,'matrimonio/matrimonio_form.html', ctx)
			
	else:
		form_matrimonio= MatrimonioFormEditar(usuario,instance=matrimonio)
		
									
	ctx = {'form_matrimonio': form_matrimonio,'notas':notas,'object':matrimonio}
	return render(request, 'matrimonio/matrimonio_form.html', ctx)



class MatrimonioListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'

	def get_queryset(self):
		try:
			parroquia = AsignacionParroquia.objects.get(
				persona__user=self.request.user).parroquia

			queryset = Matrimonio.objects.filter(parroquia=parroquia)
			return queryset
		except: 
			return [];


# VISTAS PARA ADMIN DE BAUTISMO

def bautismo_create_view(request):
	usuario=request.user
	if(request.method == 'POST' ):
	
		formBautismo=BautismoForm(usuario,request.POST)
		# form_nota=NotaMarginalForm(request.POST)
		if (formBautismo.is_valid()):
			#perfil=formPerfil.save(commit=False)
			bautismo=formBautismo.save(commit=False)
			# nota=form_nota.save(commit=False)
			bautismo.tipo_sacramento =  u'Bautismo'
			# nota.save()
			# bautismo.nota_marginal=nota
			parroquia = AsignacionParroquia.objects.get(
				persona__user=request.user,estado=True).parroquia
			bautismo.parroquia = parroquia
			bautismo.save()
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/bautismo')
		else:
			messages.error(request,formBautismo.errors)
	else:
		
		formBautismo=BautismoForm(usuario,)
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
		bautismo_form = BautismoFormEditar(usuario,request.POST or None,instance=bautismo)
		# form_nota=NotaMarginalForm(request.POST,instance=nota)
		if bautismo_form.is_valid():
			bautismo_form.save()
			messages.success(request,'Actualizado exitosamente')
			return HttpResponseRedirect('/bautismo')
		else:
			messages.error(request, 'Error al actualizar')
			ctx = {'formBautismo': bautismo_form,'notas':notas,'object':bautismo}
			return render(request, 'bautismo/bautismo_form.html', ctx)
			
	else:
		bautismo_form = BautismoFormEditar(usuario,instance=bautismo)
		
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
			parroquia = AsignacionParroquia.objects.get(persona__user=self.request.user).parroquia
			queryset = Bautismo.objects.filter(parroquia=parroquia)
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
		form_eucaristia=EucaristiaForm(usuario,request.POST)
		if form_eucaristia.is_valid():
			eucaristia=form_eucaristia.save(commit=False)
			tipo_sacramento=u'Eucaristia'
			eucaristia.tipo_sacramento=tipo_sacramento
			parroquia = AsignacionParroquia.objects.get(
				persona__user=request.user,estado=True).parroquia
			eucaristia.parroquia = parroquia
			eucaristia.save()
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/eucaristia')
		else:
			messages.error(request,form_eucaristia.errors)
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
		form_eucaristia=EucaristiaFormEditar(usuario,request.POST,instance=eucaristia)
		if(form_eucaristia.is_valid()):
			form_eucaristia.save()
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/eucaristia')
		else:
			messages.error(request,form_eucaristia.errors)
		
	else:
		form_eucaristia=EucaristiaFormEditar(usuario,instance=eucaristia)
	ctx={'form_eucaristia':form_eucaristia, 'object':eucaristia}
	return render(request,'eucaristia/eucaristia_form.html',ctx)



class EucaristiaListView(ListView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_list.html'
	def get_queryset(self):
		try:
			parroquia = AsignacionParroquia.objects.get(persona__user=self.request.user).parroquia
			queryset = Eucaristia.objects.filter(parroquia=parroquia)
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

	if(request.method == 'POST'):
		form_confirmacion=ConfirmacionForm(usuario,request.POST)
		if(form_confirmacion.is_valid()):
			confirmacion=form_confirmacion.save(commit=False)
			confirmacion.tipo_sacramento='Confirmacion'
			parroquia = AsignacionParroquia.objects.get(
				persona__user=request.user,estado=True).parroquia
			confirmacion.parroquia = parroquia
			confirmacion.save()
			messages.success(request,'Creado exitosamente')
			return HttpResponseRedirect('/confirmacion')
		else:
			messages.error(request,form_confirmacion.errors)
			
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
		form_confirmacion=ConfirmacionFormEditar(usuario,request.POST,instance=confirmacion)
		if(form_confirmacion.is_valid()):
			form_confirmacion.save()
			messages.success(request,'Actualizado exitosamente')
			return HttpResponseRedirect('/confirmacion')
		else:
			messages.error(request,form_confirmacion.errors)
	else:
		form_confirmacion=ConfirmacionFormEditar(usuario,instance=confirmacion)
	ctx={'form_confirmacion':form_confirmacion,'object':confirmacion}
	return render(request,'confirmacion/confirmacion_form.html',ctx)


class ConfirmacionListView(ListView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_list.html'

	def get_queryset(self):
		try:
			parroquia = AsignacionParroquia.objects.get(persona__user=self.request.user).parroquia
			queryset = Confirmacion.objects.filter(parroquia=parroquia)
			return queryset
		except: 
			return [];



#Vistas para crear una parroquia
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

	

class ParroquiaListView(ListView):
	model= Parroquia
	template_name = 'parroquia/parroquia_list.html'


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





def intencion_create_view(request):
	template_name = 'intencion/intencion_form.html'
	success_url = '/intencion/'
	if request.method == 'POST':
		form_intencion = IntencionForm(request.POST)
		if form_intencion.is_valid():
			intencion = form_intencion.save(commit=False)
			try:
				intencion.parroquia = AsignacionParroquia.objects.get(persona__user=request.user).parroquia
			
			except:
				raise Http404
			intencion.save()
			messages.success(request, 'Creado exitosamente')
			return HttpResponseRedirect(success_url)
		else:
			messages.error(request, u'Uno o más campos no son incorrectos: %s' % form_intencion.errors)
			ctx = {'form': form_intencion}
			return render(request, template_name, ctx)
	else:
		form_intencion = IntencionForm()
		ctx = {'form': form_intencion}
		return render(request, template_name, ctx)

class IntencionListView(ListView):
	model= Intenciones
	template_name = 'intencion/intencion_list.html'

class IntencionUpdateView(UpdateView):
	model= Intenciones
	template_name = 'intencion/intencion_form.html'
	form_class = IntencionForm
	success_url = '/intencion/'
	context_object_name = 'form_intencion'

@login_required(login_url='/login/')
@permission_required('sacramentos.can_change', login_url='/login/')
# @staff_member_required
# @user_passes_test(lambda u: u.is_staff)
def sacerdote_create_view(request):
	template_name = 'usuario/sacerdote_form.html' 
	success_url = '/sacerdote/'
	if request.method == 'POST':
		form_sacerdote = SacerdoteForm(request.POST)
		form_usuario = UsuarioForm(request.POST)
		if form_sacerdote.is_valid() and form_usuario.is_valid():
			sacerdotes, created = Group.objects.get_or_create(name='Sacerdotes')
			usuario = form_usuario.save(commit= False) 
			sacerdote = form_sacerdote.save(commit=False)
			usuario.username= sacerdote.crear_username(usuario.first_name, usuario.last_name)
			usuario.save()
			usuario.groups.add(sacerdotes)
			sacerdote.user =usuario
			sacerdote.sexo = 'm'
			sacerdote.profesion = 'Sacerdote'
			estado_civil = 's'
			sacerdote.save()
			return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Uno o más datos son inválidos')
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
			return render(request, template_name, ctx)

	else:
		form_sacerdote = SacerdoteForm()
		form_usuario = UsuarioForm()
		ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
		return render(request, template_name, ctx)

def sacerdote_update_view(request, pk):
	sacerdote = get_object_or_404(PerfilUsuario, pk=pk)
	if sacerdote.profesion != 'Sacerdote':
		raise Http404
	else: 
		template_name = 'usuario/sacerdote_form.html' 
		success_url = '/sacerdote/'
		if request.method == 'POST':
			form_sacerdote = SacerdoteForm(request.POST, instance=sacerdote)
			form_usuario = UsuarioForm(request.POST, instance=sacerdote.user)
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
			form_usuario = UsuarioForm(instance=sacerdote.user)
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
			return render(request, template_name, ctx)


class SacerdoteListView(ListView):
	model = PerfilUsuario
	template_name = 'usuario/sacerdote_list.html'
	queryset = PerfilUsuario.objects.sacerdotes()

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.can_change', login_url='/login/'))
	def dispatch(self, *args, **kwargs):
		return super(SacerdoteListView, self).dispatch(*args, **kwargs)


class AsignarParroquiaCreate(CreateView):
	model = AsignacionParroquia
	form_class = AsignarParroquiaForm
	template_name = 'parroquia/asignar_parroquia_form.html'
	success_url = '/asignar/parroquia/'

class AsignarParroquiaUpdate(UpdateView):
	model = AsignacionParroquia
	form_class = AsignarParroquiaForm
	template_name = 'parroquia/asignar_parroquia_form.html'
	success_url = '/asignar/parroquia/'	

class AsignarParroquiaList(ListView):
	model = AsignacionParroquia
	template_name = 'parroquia/asignar_parroquia_list.html'




#Reportes


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
	cura=AsignacionParroquia.objects.get(parroquia=matrimonio.parroquia).persona
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	html = render_to_string('matrimonio/matrimonio_certificado.html', {'pagesize':'A4', 
		'matrimonio':matrimonio,'cura':cura,'notas':notas},
		context_instance=RequestContext(request))
	return generar_pdf(html)

def matrimonio_acta(request, pk):
	matrimonio=get_object_or_404(Matrimonio, pk=pk)
	cura=AsignacionParroquia.objects.get(parroquia=matrimonio.parroquia).persona
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	html = render_to_string('matrimonio/matrimonio_acta.html', {'pagesize':'A4', 
		'matrimonio':matrimonio,'cura':cura,'notas':notas},
		context_instance=RequestContext(request))
	return generar_pdf(html)

def bautismo_certificado(request, pk):
	bautismo=get_object_or_404(Bautismo, pk=pk)
	cura=AsignacionParroquia.objects.get(parroquia=bautismo.parroquia).persona
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('bautismo/bautismo_certificado.html', {'pagesize':'A4', 'bautismo':bautismo,
		'cura':cura,'notas':notas},context_instance=RequestContext(request))
	return generar_pdf(html)

def bautismo_acta(request, pk):
	bautismo=get_object_or_404(Bautismo, pk=pk)
	cura=AsignacionParroquia.objects.get(parroquia=bautismo.parroquia).persona
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('bautismo/bautismo_acta.html', {'pagesize':'A4', 'bautismo':bautismo,
		'cura':cura,'notas':notas},context_instance=RequestContext(request))
	return generar_pdf(html)

def confirmacion_reporte(request, pk):
	confirmacion=get_object_or_404(Confirmacion, pk=pk)
	cura=AsignacionParroquia.objects.get(parroquia=confirmacion.parroquia).persona
	# notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('confirmacion/confirmacion_reporte.html', 
		{'pagesize':'A4', 'confirmacion':confirmacion,'cura':cura},context_instance=RequestContext(request))
	return generar_pdf(html)


def eucaristia_reporte(request, pk):
	eucaristia=get_object_or_404(Eucaristia, pk=pk)
	cura=AsignacionParroquia.objects.get(parroquia=eucaristia.parroquia).persona
	# notas=NotaMarginal.objects.filter()
	html = render_to_string('eucaristia/eucaristia_reporte.html', {'pagesize':'A4', 'eucaristia':eucaristia,
		'cura':cura},context_instance=RequestContext(request))
	return generar_pdf(html)

