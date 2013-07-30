# Create your views here.
import json

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User

from .models import PerfilUsuario,Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion
from .forms import (
	UsuarioForm, PerfilUsuarioForm, PadreForm,
	MatrimonioForm,BautismoForm,EucaristiaForm,ConfirmacionForm,
	LibroForm,
	)



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

def edit_usuario_view(request,pk):
	perfil= get_object_or_404(PerfilUsuario, pk=pk)
	user= perfil.user	
	if request.method == 'POST':
		usuario_form = UsuarioForm(request.POST,instance=user)
		perfil_form = PerfilUsuarioForm(request.POST,instance=perfil)
		if usuario_form.is_valid() and perfil_form.is_valid():
			usuario_form.save()
			perfil_form.save()
			return HttpResponseRedirect('/usuario')

	else:
		usuario_form = UsuarioForm(instance=user)
		perfil_form = PerfilUsuarioForm(instance=perfil)
									
	ctx = {'usuario_form': usuario_form,'perfil_form':perfil_form}
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

class LibroCreateView(CreateView):
	model = Libro
	form_class = LibroForm
	template_name = 'libro/libro_form.html'
	success_url= '/libro/'

class LibroUpdateView(UpdateView):
	model = Libro
	form_class=LibroForm
	template_name = 'libro/libro_form.html'
	success_url = '/libro/'

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

class MatrimonioCreateView(CreateView):
	model=Matrimonio
	form_class=MatrimonioForm
	template_name='matrimonio/matrimonio_form.html'
	success_url='/matrimonio/'


class MatrimonioUpdateView(UpdateView):
	model=Matrimonio
	template_name='matrimonio/matrimonio_form.html'
	success_url='/matrimonio/'


class MatrimonioListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'


# VISTAS PARA ADMIN DE BAUTISMO


def bautismo_create_view(request):
	if(request.method == 'POST' ):
		#formUser=UsuarioForm(request.POST)
		formPerfil=PerfilUsuarioForm(request.POST)
		formBautismo=BautismoForm(request.POST)
		if(formPerfil.is_valid() and formBautismo.is_valid()):
			# user=formUser.save(commit=False)
			perfil=formPerfil.save(commit=False)
			bautismo=formBautismo.save(commit=False)
			# user.save()
			# perfil.user=user.id
			perfil.save()
			bautismo.bautizado=perfil
			bautismo.save()
			return HttpResponseRedirect('/bautismo')
	else:
		# formUser=UsuarioForm()
		formPerfil=PerfilUsuarioForm()
		formBautismo=BautismoForm()
	ctx={'formPerfil':formPerfil,'formBautismo':formBautismo}
	return render (request,'bautismo/bautismo_form.html',ctx)



# class BautismoCreateView(CreateView):
# 	model=Bautismo
# 	template_name='bautismo/bautismo_form.html'
# 	form_class=BautismoForm
# 	success_url='/bautismo/'


class BautismoUpdateView(UpdateView):
	model=Bautismo
	template_name='bautismo/bautismo_form.html'
	#form_class=BautismoForm
	success_url='/bautismo/'

class BautismoListView(ListView):
	model=Bautismo
	template_name='bautismo/bautismo_list.html'



# VISTAS PARA ADMIN DE EUCARISTIA

class EucaristiaCreateView(CreateView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_form.html'
	success_url='/eucaristia/'


class EucaristiaUpdateView(UpdateView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_form.html'
	success_url='/eucaristia/'

class EucaristiaListView(ListView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_list.html'

# VISTAS PARA ADMIN DE CONFIRMACION

class ConfirmacionCreateView(CreateView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_form.html'
	success_url='/confirmacion/'

class ConfirmacionUpdateView(UpdateView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_form.html'
	success_url='/confirmacion/'

class ConfirmacionListView(ListView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_list.html'
