# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import RadioSelect

from .models import (PerfilUsuario, 
					Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,Bautismo,
					Direccion)


#forms para manejo de usuarios
class UsuarioForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres', 
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos', 
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name')

class PerfilUsuarioForm(ModelForm):
	SEXO_CHOICES = (
		('Masculino', 'Masculino'),
		('Femenino', 'Femenino'),
		)
	fecha_nacimiento = forms.CharField(required=True, label=u'Fecha de Nacimiento', 
		widget=forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	sexo = forms.ChoiceField(label=u'Sexo', choices=SEXO_CHOICES, required=True, 
		widget=forms.RadioSelect(attrs={'required':''}))
	class Meta():
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil' ,'profesion', 
			'padre', 'madre');

class PadreForm(ModelForm):
	fecha_nacimiento = forms.CharField(label='Fecha de Nacimiento',
		widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	lugar_nacimiento = forms.CharField(label='Lugar de Nacimiento')
	class Meta(): 
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil', 'profesion');

# forms para sacramentos

class LibroForm(ModelForm):
	TIPO_LIBRO_CHOICES = (
		('Bautismo','Bautismo'),
        ('Eucaristia','Eucaristia'), 
        ('Confirmacion','Confirmacion'),
        ('Matrimonio','Matrimonio'),
        ('Intenciones','Intenciones')          
    )
	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	numero_libro=forms.IntegerField(required=True, label='Numero Libro', 
		widget=forms.TextInput(attrs={'required': ''}))

	# tipo_libro = forms.ChoiceField(label=u'Tipo de Libro', choices=TIPO_LIBRO_CHOICES, required=True,
	# widget=forms.Select(attrs={'required':'','type':'select'}))

	estado=forms.ChoiceField(required=True,choices=ESTADO_CHOICES,label='Estado',
		widget=RadioSelect(attrs={'required':''}))
	fecha_apertura = forms.CharField(required=True, label=u'Fecha de Apertura', 
		widget=forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'
			}))
	fecha_cierre = forms.CharField(required=True, label=u'Fecha de Cierre', 
		widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'
			}))
	numero_maximo_actas=forms.IntegerField(required=True, label='Maximo Actas', 
		widget=forms.TextInput(attrs={'required': '','type':'number','value':'35','max':'40'}))
	
	class Meta():
		model=Libro

class MatrimonioForm(ModelForm):
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}))
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}))
	testigo_novio= forms.CharField(required=True,label='Testigo',
		widget=forms.TextInput(attrs={'required':''}))
	testigo_novia= forms.CharField(required=True,label='Testiga',
		widget=forms.TextInput(attrs={'required':''}))
	class Meta():
		model=Matrimonio
		fields=('numero_acta','pagina','libro','fecha_sacramento','lugar_sacramento','padrino','madrina',
			'iglesia','novio','novia','testigo_novio','testigo_novia')

	# def __init__(self,*args,**kwargs):
	# 	super(LibroForm,self).__init__(*args,**kwargs)
	# 	if (libro.tipo_libro=='Bautismo'):
	# 		self.fields['libro'].queryset = User.objects.filter(tipo_libro='Matrimonio')

class BautismoForm(ModelForm):
	# bautizado=forms.CharField(widget=forms.TextInput())
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}))
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}))
	libro=forms.ModelChoiceField(required=True,label='Libross',queryset=Libro.objects.none())
	class Meta():
		model=Bautismo
		fields=('numero_acta','pagina','bautizado','libro','fecha_sacramento','lugar_sacramento','padrino','madrina',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno','abuela_materna','vecinos_paternos','vecinos_maternos')

class EucaristiaForm(ModelForm):
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}))
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}))
	class Meta():
		model=Eucaristia
		fields=('numero_acta','pagina','feligres','libro','fecha_sacramento','lugar_sacramento','padrino',
			'madrina','iglesia')

class ConfirmacionForm(ModelForm):
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}))
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}))
	obispo = forms.CharField(required=True,label='Celebrante',
		widget=forms.TextInput(attrs={'required':''}))
	class Meta():
		model=Confirmacion
		fields=('numero_acta','pagina','confirmado','libro','fecha_sacramento','lugar_sacramento','padrino',
			'madrina','obispo','iglesia')



#Forms para dirección
class DireccionForm(ModelForm):
	class Meta:
		model = Direccion

