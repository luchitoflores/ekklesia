from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import RadioSelect

from .models import PerfilUsuario, Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion

class UsuarioForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres', widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos', widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name')

class PerfilUsuarioForm(ModelForm):
	SEXO_CHOICES = (
		('Masculino', 'Masculino'),
		('Femenino', 'Femenino'),
		)
	fecha_nacimiento = forms.CharField(required=True, label=u'Fecha de Nacimiento', widget=forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	sexo = forms.ChoiceField(label=u'Sexo', choices=SEXO_CHOICES, required=True, widget=forms.RadioSelect(attrs={'required':''}))
	class Meta():
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil' ,'profesion', 'padre', 'madre');

class PadreForm(ModelForm):
	fecha_nacimiento = forms.CharField(label='Fecha de Nacimiento',widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	lugar_nacimiento = forms.CharField(label='Lugar de Nacimiento')
	class Meta(): 
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil', 'profesion');

class LibroForm(ModelForm):
	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	estado=forms.ChoiceField(choices=ESTADO_CHOICES,widget=RadioSelect)
	class Meta():
		model=Libro

class MatrimonioForm(ModelForm):
	class Meta():
		model=Matrimonio
		fields=('numero_acta','pagina','fecha_sacramento','lugar_sacramento','padrino','madrina',
			'iglesia','novio','novia','testigo_novio','testigo_novia')

class BautismoForm(ModelForm):
	# bautizado=forms.CharField(widget=forms.TextInput())
	class Meta():
		model=Bautismo
		fields=('numero_acta','pagina','bautizado','fecha_sacramento','lugar_sacramento','padrino','madrina',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno','abuela_materna','vecinos_paternos','vecinos_maternos')

class EucaristiaForm(ModelForm):
	class Meta():
		model=Eucaristia
		fields=('numero_acta','pagina','feligres','fecha_sacramento','lugar_sacramento','padrino',
			'madrina','iglesia')

class ConfirmacionForm(ModelForm):
	class Meta():
		model=Confirmacion
		fields=('numero_acta','pagina','confirmado','fecha_sacramento','lugar_sacramento','padrino',
			'madrina','obispo','iglesia')


