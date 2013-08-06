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
	class Meta:
		model = Direccion