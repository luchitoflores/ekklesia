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
	telefono=forms.CharField(label='Telefono')
	celular=forms.CharField(label='Celular')
	
	queryset_canton = Canton.objects.all()
	queryset_parroquia = Parroquia.objects.all()
	def __init__(self, canton = queryset_canton, parroquia = queryset_parroquia, *args, **kwargs):
		# queryset_canton = kwargs.pop('queryset')
		super(DireccionForm, self).__init__(*args, **kwargs)	
		self.fields['canton']=forms.ModelChoiceField(queryset=canton, empty_label='-- Seleccione --', widget=forms.Select(attrs={'required':'', 'disabled':''}))
		self.fields['parroquia']= forms.ModelChoiceField(queryset=parroquia, empty_label='-- Seleccione --', widget=forms.Select(attrs={'required':'', 'disabled':''}))
		# self.fields['canton'] = forms.ModelChoiceField(queryset=Canton.objects.all())


	class Meta:
		model = Direccion

