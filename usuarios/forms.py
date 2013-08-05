# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField

from .models import Usuario

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Clave', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirme su clave', widget=forms.PasswordInput)

	class Meta:
		model = Usuario

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Las claves deben ser iguales")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text= ("Si desea puede cambiar la contraseña aquí: <a href=\"password/\">Cambiar contrseña</a>."))
	class Meta:
		model = Usuario

	def clean_password(self):
		return self.initial["password"]
