# -*- coding:utf-8 -*-
from django.forms import ModelForm
from django import forms
from .models import Provincia, Canton, Parroquia, Direccion
from django.forms.widgets import *


class ProvinciaForm(ModelForm):
	# nombre = forms.CharField(required=True, label='Nombre', 
	# 	help_text='Ingrese los nombres completos. Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))
	# abreviatura = forms.CharField(required=True, label='Abreviatura', 
	# 	help_text='Ingrese los nombres completos. Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))

	class Meta:
		model = Provincia
		
		


class CantonForm(ModelForm):
	# nombre = forms.CharField(required=True, label='Nombre', 
	# 	help_text='Ingrese los nombres completos. Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))
	# abreviatura = forms.CharField(required=True, label='Abreviatura', 
	# 	help_text='Ingrese los nombres completos. Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))
	# provincia = forms.ModelChoiceField(required=True, label='Abreviatura', 
	# 	empty_label='-- Seleccione --' ,queryset=None, help_text='Ingrese los nombres completos.'+
	# 	' Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))

	class Meta:
		model = Canton
       

class ParroquiaForm(ModelForm):
	# nombre = forms.CharField(required=True, label='Nombre', 
	# 	help_text='Ingrese los nombres completos. Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))
	# abreviatura = forms.CharField(required=True, label='Abreviatura', 
	# 	help_text='Ingrese los nombres completos. Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))
	# canton = forms.ModelChoiceField(required=True, label='Abreviatura', 
	# 	empty_label='-- Seleccione --' ,queryset=None, help_text='Ingrese los nombres completos.'+
	# 	' Ej: Juan José',
	# 	widget=forms.TextInput(attrs={'required': ''}))
	class Meta:
		model = Parroquia
		fields = ('nombre','abreviatura','canton')
       
# Forms para dirección

class DireccionForm(ModelForm):
	
    domicilio=forms.CharField(label='Domicilio', max_length=200, required=True,
		help_text='Ingrese la direccion Ej: Sucre 7-19 y Lourdes',
		widget=forms.TextInput(attrs={'required': ''}))
    provincia=forms.ModelChoiceField(queryset=Provincia.objects.all(), empty_label='-- Seleccione --',
    	help_text='Seleccione una provincia Ej: Loja, El Oro',
    	widget=forms.Select(attrs={'required':''}))
    telefono=forms.CharField(label='Telefono', help_text='Ingrese un tel convencional'+
		' Ej: 072588278')
		
    queryset_canton = Canton.objects.all()
    queryset_parroquia = Parroquia.objects.all()
    def __init__(self, canton = queryset_canton, parroquia = queryset_parroquia, *args, **kwargs):
	super(DireccionForm, self).__init__(*args, **kwargs)	
	self.fields['canton']=forms.ModelChoiceField(queryset=canton, empty_label='-- Seleccione --',
		help_text='Seleccione un canton Ej: Loja - Calvas', 
		widget=forms.Select(attrs={'required':'', 'disabled':''}))
	self.fields['parroquia']= forms.ModelChoiceField(queryset=parroquia,
		empty_label='-- Seleccione --', help_text='Seleccione una parroquia Ej: El Sagrario',
		widget=forms.Select(attrs={'required':'', 'disabled':''}))
		


    class Meta:
	model = Direccion

