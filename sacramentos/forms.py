from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import RadioSelect

from .models import PerfilUsuario, Libro

class UsuarioForm(ModelForm):
	class Meta:
		model = User
		fields= ('first_name', 'last_name')

class PerfilUsuarioForm(ModelForm):
	class Meta:
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'profesion');


class LibroForm(ModelForm):
	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	estado=forms.ChoiceField(choices=ESTADO_CHOICES,widget=RadioSelect)
	class Meta:
		model=Libro


