from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import RadioSelect

from .models import PerfilUsuario, Libro

class UsuarioForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres')
	last_name = forms.CharField(required=True, label='Apellidos')

	class Meta:
		model = User
		fields= ('first_name', 'last_name')

class PerfilUsuarioForm(ModelForm):
	class Meta:
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil' ,'profesion');

class PadreForm(ModelForm):
	fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento')
	lugar_nacimiento = forms.CharField(label='Lugar de Nacimiento')
	class Meta: 
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil', 'profesion');

class LibroForm(ModelForm):
	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	estado=forms.ChoiceField(choices=ESTADO_CHOICES,widget=RadioSelect)
	class Meta:
		model=Libro

