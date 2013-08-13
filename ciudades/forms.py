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
        fields = ('nombre',)

# Forms para dirección
class DireccionForm(ModelForm):
	domicilio=forms.CharField(label='Domicilio', max_length=200, required=True)
	provincia=forms.ModelChoiceField(queryset=Provincia.objects.all(), empty_label='-- Seleccione --', widget=forms.Select(attrs={'required':''}))
	canton=forms.ModelChoiceField(queryset=Canton.objects.all(), empty_label='-- Seleccione --', widget=forms.Select(attrs={'required':'', 'disabled':''}))
	parroquia=forms.ModelChoiceField(queryset=Parroquia.objects.all(), empty_label='-- Seleccione --',  widget=forms.Select(attrs={'required':'', 'disabled':''}))
	telefono=forms.CharField(label='Telefono')
	celular=forms.CharField(label='Celular', initial='0999999')
	
	class Meta:
		model = Direccion


# class DireccionForm(ModelForm):
# 	domicilio=forms.CharField(label='Domicilio', max_length=200, required=True)
# 	telefono=forms.CharField(label='Telefono', max_length=200, required=True)
# 	celular=forms.CharField(label='Celular', max_length=200, required=True)
# 	provincia=forms.ModelChoiceField(queryset=Provincia.objects.all(), empty_label='-- Seleccione --', widget=forms.Select(attrs={'required':''}))
# 	queryset_provincia = Provincia.objects.all()
# 	# queryset_canton = Canton.objects.all()
# 	queryset_parroquia = Parroquia.objects.all()



# 	def __init__(self, *args, **kwargs):
# 		queryset_canton = kwargs.pop('queryset')
# 		super(DireccionForm, self).__init__(self, *args, **kwargs)	
# 		self.fields['canton'] = forms.ModelChoiceField(queryset=Canton.objects.all())
	
# 	class Meta:
# 		model = Direccion
