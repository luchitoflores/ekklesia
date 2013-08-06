# -*- coding:utf-8 -*-
from django.forms import ModelForm
from django import forms
from .models import Provincia, Canton, Parroquia, Direccion
from django.forms.widgets import *


class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia


class CantonForm(forms.ModelForm):
    class Meta:
        model = Canton

class ParroquiaForm(forms.ModelForm):
    class Meta:
        model = Parroquia

#Forms para dirección
class DireccionForm(ModelForm):
	CHOICES_DEFAULT = (('', '---------'),)
	nombre=forms.CharField(label='Nombre', max_length=200, required=True)
	# provincia=forms.ChoiceField(label='Nombre')
	# canton=forms.ChoiceField(label='Canton', required=True, widget=forms.Select(attrs={'required':'', 'disabled':''}))
	# parroquia=forms.ChoiceField(label='Parroquia', widget=forms.Select(attrs={'required':'', 'disabled':''}))
	telefono=forms.CharField(label='Telefono')
	celular=forms.CharField(label='Celular')
	
	class Meta:
		model = Direccion