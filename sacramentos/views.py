# Create your views here.
import json

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import (PerfilUsuario,
	Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,
	Parroquia, Intenciones)

from .forms import (
	UsuarioForm, PerfilUsuarioForm, PadreForm,
	MatrimonioForm,BautismoForm,EucaristiaForm,ConfirmacionForm,
	LibroForm,
	DivErrorList,
	)



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

def usuarioCreateView(request):
	if request.method == 'POST':
		valido = False
		form_usuario = UsuarioForm(request.POST)
		form_perfil = PerfilUsuarioForm(request.POST, error_class=DivErrorList)
		if form_usuario.is_valid() and form_perfil.is_valid():
			valido = True
			usuario = form_usuario.save(commit=False)
			perfil = form_perfil.save(commit=False)
			usuario.username = perfil.dni
			usuario.save()
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
		if(form_libro.is_valid()):
			libro=form_libro.save(commit=False)
			estado=libro.estado
			tipo=libro.tipo_libro

			try:

				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo)
				if(estado != consulta.estado and tipo!=consulta.tipo_libro):
					if libro.fecha_cierre_mayor():

						libro.save()
						return HttpResponseRedirect('/libro')
					else:
						messages.add_message(request,messages.WARNING,
						{'Fecha':'La fecha de cierre no puede ser menor o igual a fecha de apertura'})

				elif(estado != consulta.estado and tipo==consulta.tipo_libro):
					if libro.fecha_cierre_mayor():
						libro.save()
						return HttpResponseRedirect('/libro')
					else:
						messages.add_message(request,messages.WARNING,
						{'Fecha':'La fecha de cierre no puede ser menor o igual a fecha de apertura'})
				else:
					messages.add_message(request,messages.WARNING,
						{'Libro':'Ya existe un libro abierto, cierrelo y vuela a crear'})

			except ObjectDoesNotExist:
				libro.save()
				return HttpResponseRedirect('/libro')
				

		else:
			messages.add_message(request,messages.WARNING,{'libro':form_libro.errors})
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

			try:

				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo)
				if(estado != consulta.estado and tipo!=consulta.tipo_libro):
					if libro.fecha_cierre_mayor():

						libro.save()
						return HttpResponseRedirect('/libro')
					else:
						messages.add_message(request,messages.WARNING,
						{'Fecha':'La fecha de cierre no puede ser menor o igual a fecha de apertura'})

				elif(estado != consulta.estado and tipo==consulta.tipo_libro):
					if libro.fecha_cierre_mayor():

						libro.save()
						return HttpResponseRedirect('/libro')
					else:
						messages.add_message(request,messages.WARNING,
						{'Fecha':'La fecha de cierre no puede ser menor o igual a fecha de apertura'})
				else:
					messages.add_message(request,messages.WARNING,
						{'Libro':'Ya existe un libro abierto, cierrelo y vuela a crear'})

			except ObjectDoesNotExist:
				libro.save()
				return HttpResponseRedirect('/libro')
				

		else:
			messages.add_message(request,messages.WARNING,{'libro':form_libro.errors})
	else:
		form_libro=LibroForm(instance=libro)
	ctx={'form_libro':form_libro}
	return render(request,'libro/libro_form.html',ctx)


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

	
# VISTAS PARA ADMIN MATRIMONIO

# class MatrimonioCreateView(CreateView):
# 	model=Matrimonio
# 	form_class=MatrimonioForm
# 	template_name='matrimonio/matrimonio_form.html'
# 	success_url='/matrimonio/'

def matrimonio_create_view(request):
	if(request.method=='POST'):
		form_matrimonio=MatrimonioForm(request.POST)
		if(form_matrimonio.is_valid()):
			matrimonio=form_matrimonio.save(commit=False)
			matrimonio.tipo_sacramento='Matrimonio'
			novio=matrimonio.novio
			novia=matrimonio.novia
			novio.estado_civil='Casado/a'
			novia.estado_civil='Casado/a'
			novio.save()
			novia.save()
			matrimonio.novio=novio
			# matrimonio.novia.estado_civil='Casado/a'
			if(matrimonio.novio.estado_civil=='Casado/a' and matrimonio.novia.estado_civil=='Casado/a'):
				matrimonio.save()
				return HttpResponseRedirect('/matrimonio')
			else:
				messages.add_message(request, messages.WARNING, {'Matrimonio':'error de estado civil'})
		else:
			messages.add_message(request, messages.WARNING, {'Matrimonio':form_matrimonio.errors})
	else:
		form_matrimonio=MatrimonioForm()
	ctx={'form_matrimonio':form_matrimonio}
	return render(request,'matrimonio/matrimonio_form.html',ctx)


# class MatrimonioUpdateView(UpdateView):
# 	model=Matrimonio
# 	template_name='matrimonio/matrimonio_form.html'
# 	success_url='/matrimonio/'

def matrimonio_update_view(request,pk):
	matrimonio=get_object_or_404(Matrimonio,pk=pk)
	if request.method == 'POST':
		form_matrimonio = MatrimonioForm(request.POST,instance=matrimonio)
		if form_matrimonio.is_valid():
			form_matrimonio.save()
			return HttpResponseRedirect('/matrimonio')
		else:
			messages.add_message(request, messages.WARNING, {'Matrimonio':form_matrimonio.errors})

	else:
		form_matrimonio= MatrimonioForm(instance=matrimonio)
									
	ctx = {'form_matrimonio': form_matrimonio}
	return render(request, 'matrimonio/matrimonio_form.html', ctx)



class MatrimonioListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'


# VISTAS PARA ADMIN DE BAUTISMO

def bautismo_create_view(request):
	if(request.method == 'POST' ):
		formBautismo=BautismoForm(request.POST)
		if formBautismo.is_valid():
			#perfil=formPerfil.save(commit=False)
			bautismo=formBautismo.save(commit=False)
			tipo_sacramento = 'Bautismo'
			bautismo.tipo_sacramento = tipo_sacramento
			bautismo.save()
			return HttpResponseRedirect('/bautismo')
		else:
			messages.add_message(request, messages.WARNING, {'Bautismo':formBautismo.errors})
	else:
		formBautismo=BautismoForm()

	ctx={'formBautismo':formBautismo}
	return render (request,'bautismo/bautismo_form.html',ctx)



# class BautismoCreateView(CreateView):
# 	model=Bautismo
# 	template_name='bautismo/bautismo_form.html'
# 	form_class=BautismoForm
# 	success_url='/bautismo/'



def bautismo_update_view(request,pk):
	bautismo= get_object_or_404(Bautismo, pk=pk)
	# perfil= bautismo.bautizado	
	if request.method == 'POST':
		bautismo_form = BautismoForm(request.POST,instance=bautismo)
		# perfil_form = PerfilUsuarioForm(request.POST,instance=perfil)
		if bautismo_form.is_valid():
			bautismo_form.save()
			# perfil_form.save()
			return HttpResponseRedirect('/bautismo')
		else:
			messages.add_message(request, messages.WARNING, {'Bautismo':bautismo_form.errors})
	else:
		bautismo_form = BautismoForm(instance=bautismo)
		# perfil_form = PerfilUsuarioForm(instance=perfil)
									
	ctx = {'formBautismo': bautismo_form}
	return render(request, 'bautismo/bautismo_form.html', ctx)



# class BautismoUpdateView(UpdateView):
# 	model=Bautismo
# 	template_name='bautismo/bautismo_form.html'
# 	success_url= '/bautismo/'

class BautismoListView(ListView):
	model=Bautismo
	template_name='bautismo/bautismo_list.html'



# VISTAS PARA ADMIN DE EUCARISTIA

# class EucaristiaCreateView(CreateView):
# 	model=Eucaristia
# 	template_name='eucaristia/eucaristia_form.html'
# 	success_url='/eucaristia/'


def eucaristia_create_view(request):
	if request.method == 'POST':
		form_eucaristia=EucaristiaForm(request.POST)
		if form_eucaristia.is_valid():
			eucaristia=form_eucaristia.save(commit=False)
			tipo_sacramento='Eucaristia'
			eucaristia.tipo_sacramento=tipo_sacramento
			eucaristia.save()
			return HttpResponseRedirect('/eucaristia')
		else:
			messages.add_message(request,messages.WARNING,{'Eucaristia':form_eucaristia.errors})
	else:
		form_eucaristia=EucaristiaForm()

	ctx={'form_eucaristia':form_eucaristia}
	return render(request,'eucaristia/eucaristia_form.html',ctx)


# class EucaristiaUpdateView(UpdateView):
# 	model=Eucaristia
# 	template_name='eucaristia/eucaristia_form.html'
# 	success_url='/eucaristia/'

def eucaristia_update_view(request,pk):
	eucaristia=get_object_or_404(Eucaristia,pk=pk)
	if(request.method == 'POST'):
		form_eucaristia=EucaristiaForm(request.POST,instance=eucaristia)
		if(form_eucaristia.is_valid()):
			form_eucaristia.save()
			return HttpResponseRedirect('/eucaristia')
		else:
			messages.add_message(request,messages.WARNING,{'Eucaristia':form_eucaristia.errors})
	else:
		form_eucaristia=EucaristiaForm(instance=eucaristia)
	ctx={'form_eucaristia':form_eucaristia}
	return render(request,'eucaristia/eucaristia_form.html',ctx)



class EucaristiaListView(ListView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_list.html'

# VISTAS PARA ADMIN DE CONFIRMACION

# class ConfirmacionCreateView(CreateView):
# 	model=Confirmacion
# 	template_name='confirmacion/confirmacion_form.html'
# 	success_url='/confirmacion/'

def confirmacion_create_view(request):
	if(request.method == 'POST'):
		form_confirmacion=ConfirmacionForm(request.POST)
		if(form_confirmacion.is_valid()):
			confirmacion=form_confirmacion.save(commit=False)
			confirmacion.tipo_sacramento='Confirmacion'
			confirmacion.save()
			return HttpResponseRedirect('/confirmacion')
		else:
			messages.add_message(request,messages.WARNING,{'Confirmacion':form_confirmacion.errors})
	else:
		form_confirmacion=ConfirmacionForm()
	ctx={'form_confirmacion':form_confirmacion}
	return render(request,'confirmacion/confirmacion_form.html',ctx)




# class ConfirmacionUpdateView(UpdateView):
# 	model=Confirmacion
# 	template_name='confirmacion/confirmacion_form.html'
# 	success_url='/confirmacion/'

def confirmacion_update_view(request,pk):
	confirmacion=get_object_or_404(Confirmacion,pk=pk)
	if(request.method == 'POST'):
		form_confirmacion=ConfirmacionForm(request.POST,instance=confirmacion)
		if(form_confirmacion.is_valid()):
			form_confirmacion.save()
			return HttpResponseRedirect('/confirmacion')
		else:
			messages.add_message(request,messages.WARNING,{'Confirmacion':form_confirmacion.errors})
	else:
		form_confirmacion=ConfirmacionForm(instance=confirmacion)
	ctx={'form_confirmacion':form_confirmacion}
	return render(request,'confirmacion/confirmacion_form.html',ctx)


class ConfirmacionListView(ListView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_list.html'



#Vistas para crear una parroquia
class ParroquiaCreateView(CreateView):
	model = Parroquia
	template_name = 'parroquia/parroquia_form.html'
	success_url = '/parroquia/'

class ParroquiaListView(ListView):
	model= Parroquia
	template_name = 'parroquia/parroquia_list.html'

class ParroquiaUpdateView(UpdateView):
	model= Parroquia
	template_name = 'parroquia/parroquia_form.html'



#Vistas para administar intenciones de misa
class IntencionCreateView(CreateView):
	model = Intenciones
	template_name = 'intencion/intencion_form.html'
	success_url = '/intencion/'

class IntencionListView(ListView):
	model= Intenciones
	template_name = 'intencion/intencion_list.html'

class IntencionUpdateView(UpdateView):
	model= Intenciones
	template_name = 'intencion/intencion_form.html'
