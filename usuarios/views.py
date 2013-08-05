# *-* coding:utf-8 *-* 
# Create your views here.
import json

from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.models import Group, User

def loginajax_view(request):	
	if request.method == 'POST':
		exito = False
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request,user)
			exito = True
			# return HttpResponseRedirect('/')
			ctx = {'exito': exito}
			return HttpResponse(json.dumps(ctx), content_type='application/json')

		else:
			ctx = {'exito': exito}
			return HttpResponse(json.dumps(ctx), content_type='application/json')


	else:
		exito = False
		ctx = json.dumps({'exito': exito})
		return HttpResponse(ctx, content_type="application/json; charset=uft8")

#Login de usuarios sin utilizar ningún formulario preestablecido
# def login_view(request):
# 	if request.user.is_authenticated():
# 		return HttpResponseRedirect('/feligres/add')
# 	else:
# 		if request.method == 'POST':
# 			username = request.POST['username']
# 			password = request.POST['password']
# 			user = authenticate(username=username, password=password)
# 			if user is not None and user.is_active:
# 				login(request,user)
# 				return HttpResponseRedirect('/')
# 			else:
# 				messages.add_message(request, messages.ERROR, 'El user o la pass son incorrectas')
# 		return render(request, 'login.html')


#Login con AthenticateForm	
def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':		
			form = AuthenticationForm(data=request.POST)
			if form.is_valid():
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)

				if user is not None and user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					messages.add_message(request, messages.ERROR, 'El user is None')
			else:
				messages.add_message(request, messages.ERROR, 'El form no es válido')
		else:
			form = AuthenticationForm()
	return render(request, 'login.html', {'form':form})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

##Cambiar la contraseña sin proporcionar la antigua contraseña
# @login_required(login_url='/login/')
# def change_password_view(request):
# 	user = request.user
# 	if request.method == 'POST':
# 		form = SetPasswordForm(user, request.POST)
# 		if form.is_valid():
# 			form.save()
# 			logout(request)
# 			messages.add_message(request, messages.INFO, 'El cambio de clave se realizó con éxito')
# 			return HttpResponseRedirect('/')
# 		else:
# 			messages.add_message(request, messages.ERROR, 'Los datos ingresados no son válidos')
# 	else:
# 		form = SetPasswordForm(user)

# 	ctx = {'form': form}
# 	return render(request, 'change-password.html', ctx)
# 	

#Cambiar la contraseña proporcionando la antigua contraseña 
@login_required(login_url='/login/')
def change_password_view(request):
	user = request.user
	if request.method == 'POST':
		form = PasswordChangeForm(user, request.POST)
		if form.is_valid():
			form.save()
			logout(request)
			messages.add_message(request, messages.INFO, 'El cambio de clave se realizó con éxito')
			return HttpResponseRedirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'Revise los errores')
	else:
		form = PasswordChangeForm(user)

	ctx = {'form': form}
	return render(request, 'change-password.html', ctx)
	

class GroupCreate(CreateView):
	model = Group
	success_url = '/group/'

	@method_decorator(login_required(login_url='login'))
	def dispatch(self, *args, **kwargs):
		return super(GroupCreate, self).dispatch(*args, **kwargs)


class GroupUpdate(UpdateView):
	"""docstring for GroupUpdate"""
	model = Group
	template_name       = 'auth/group_form.html'
	context_object_name = 'form'
	success_url = '/group/'

	@method_decorator(login_required(login_url='login'))
	def dispatch(self, *args, **kwargs):
		return super(GroupUpdate, self).dispatch(*args, **kwargs)

class GroupList(ListView):
	model = Group
	context_object_name = 'object_list'
	template_name = 'auth/group_list.html'

	
		

	
		

