# -*- coding:utf-8 -*-
from django.contrib import messages
from datetime import datetime, date
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.forms.widgets import RadioSelect

from .models import (PerfilUsuario, 
					Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,Bautismo,
					Direccion, Intenciones,NotaMarginal,Parroquia,AsignacionParroquia)



class DivErrorList(ErrorList):
	def __unicode__(self):
		return self.as_divs()

	def as_divs(self):
		if not self: 
			return u''
		return u'<div class="error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


#forms para manejo de usuarios
class UsuarioForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres', help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos', help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'groups')
		widgets = {
			'groups': forms.CheckboxSelectMultiple(attrs={'required':''})
		}


class UsuarioPadreForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres', help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos', help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name')
		

class PerfilUsuarioForm(ModelForm):

	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	# error_css_class = 'errorprueba'
	# required_css_class = 'requiredeeeee'

	SEXO_CHOICES = (
		('', '--- Seleccione ---'),
		('m', 'Masculino'),
		('f', 'Femenino'),
		)

	ESTADO_CIVIL_CHOICES    = (
		('', '--- Seleccione ---'),
		('s','Soltero/a'),
		('c','Casado/a'),
		('d','Divorciado/a'),
		('v','Viudo/a')
		)
	# fecha_nacimiento = forms.CharField(required=True, label=u'Fecha de Nacimiento', 
	sexo = forms.TypedChoiceField(label=u'Sexo', help_text='Elija el sexo de la persona. Ej: Masculino', choices=SEXO_CHOICES, required=True, widget=forms.Select(attrs={'required':''}))
	estado_civil = forms.TypedChoiceField(label=u'Estado Civil', help_text='Elija el estado civil. Ej: Soltero/a', choices=ESTADO_CIVIL_CHOICES, required=True, widget=forms.Select(attrs={'required':''}))
	# padre= forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), empty_label='--- Seleccione ---')
	# madre= forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), empty_label='--- Seleccione ---')
		
	class Meta():
		model = PerfilUsuario
		fields = ('nacionalidad', 'dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil' ,'profesion', 'padre', 'madre');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			'dni': forms.TextInput(attrs={'required':''}),
			# 'estado_civil': forms.Select(attrs={'required':''}),
			# 'sexo': forms.Select(attrs={'required':''}),
		}
		
class PadreForm(ModelForm):
	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	# fecha_nacimiento = forms.CharField(label='Fecha de Nacimiento', help_text='Ingrese la fecha de nacimiento con formato dd/mm/yyyy',
	# 	widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	# lugar_nacimiento = forms.CharField(label='Lugar de Nacimiento', help_text='Ingrese el lugar de Nacimiento. Ej: Amaluza')
	
	class Meta(): 
		model = PerfilUsuario
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil',
		 'profesion');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			}


class SacerdoteForm(ModelForm):
	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	# fecha_nacimiento = forms.CharField(help_text='Ingrese la fecha de nacimiento con formato dd/mm/yyyy', label='Fecha de Nacimiento',
	# 	widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	# lugar_nacimiento = forms.CharField(help_text='Ingrese el lugar de Nacimiento. Ej: Amaluza', label='Lugar de Nacimiento')
	class Meta(): 
		model = PerfilUsuario
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			}




# forms para sacramentos

class LibroForm(ModelForm):
	TIPO_LIBRO_CHOICES = (
		('', '--- Seleccione ---'),
		('Bautismo','Bautismo'),
        ('Eucaristia','Eucaristia'), 
        ('Confirmacion','Confirmacion'),
        ('Matrimonio','Matrimonio'),
                 
    )
	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	numero_libro=forms.IntegerField(required=True, label='Numero Libro', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese un numero para libro ej:1,35')

	tipo_libro= forms.TypedChoiceField(label=u'Tipo de Libro', choices=TIPO_LIBRO_CHOICES, 
		required=True, widget=forms.Select(attrs={'required':''}),
		help_text='Seleccione un tipo de libro')

	estado=forms.ChoiceField(required=True,choices=ESTADO_CHOICES,label='Estado', 
		widget=RadioSelect(attrs={'required':''}))
	fecha_apertura = forms.CharField(label=u'Fecha de Apertura', initial=date.today(),
		widget=forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:17/12/2010')
	fecha_cierre = forms.CharField(required=False,label=u'Fecha de Cierre', 
		widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'
			}),help_text='Seleccione una fecha ej:17/12/2010')
	numero_maximo_actas=forms.IntegerField(required=True, label='Maximo Actas', 
		widget=forms.TextInput(attrs={'required': '','type':'number','value':'35',
			'max':'40'}),help_text='Ingrese el numero maximo de actas ej:50') 
	
	class Meta():
		model=Libro
		fields = ('numero_libro', 'tipo_libro', 'fecha_apertura', 'fecha_cierre', 
			'estado', 'numero_maximo_actas')



class BautismoForm(ModelForm):
	bautizado=forms.ModelChoiceField(
		label='Feligres',
		help_text='Presione buscar para encontrar un feligres',
		queryset=PerfilUsuario.objects.todos(),	required=True,	empty_label='--- Seleccione ---',
		widget=forms.Select(attrs={'required':''}))
	pagina=forms.IntegerField(required=True,help_text='Ingrese el numero de pagina ej:5,67', label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(help_text='Ingrese el numero del acta ej:3,25',
		required=True, 
		label='Numero Acta', widget=forms.TextInput(attrs={'required': ''}))
	fecha_sacramento = forms.CharField(help_text='Seleccione una fecha ej:18/07/2000',
		required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}))
	lugar_sacramento = forms.CharField(help_text='Ingrese el lugar del sacramento ej: Loja ', 
		required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(help_text='Ingrese el nombre de la iglesia: San Jose',
		required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}))
	libro=forms.ModelChoiceField(help_text='Seleccione un libro para el Bautismo',
		queryset=Libro.objects.none(),empty_label=None)

	def __init__(self,user, *args, **kwargs):

		super(BautismoForm, self).__init__(*args, **kwargs)
		
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Bautismo',parroquia=parroquia)
      	
	class Meta():
		model=Bautismo
		fields=('numero_acta','pagina','bautizado','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')

class BautismoFormEditar(ModelForm):
	bautizado=forms.ModelChoiceField(
		label='Feligres',
		help_text='Presione buscar para encontrar un feligres',
		queryset=PerfilUsuario.objects.todos(),	required=True,	empty_label='--- Seleccione ---',
		widget=forms.Select(attrs={'required':''}))
	pagina=forms.IntegerField(required=True,help_text='Ingrese el numero de pagina ej:5,67', label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(help_text='Ingrese el numero del acta ej:3,25',
		required=True, 
		label='Numero Acta', widget=forms.TextInput(attrs={'required': ''}))
	fecha_sacramento = forms.CharField(help_text='Seleccione una fecha ej:18/07/2000',
		required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}))
	lugar_sacramento = forms.CharField(help_text='Ingrese el lugar del sacramento ej: Loja ', 
		required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(help_text='Ingrese el nombre de la iglesia: San Jose',
		required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}))
	libro=forms.ModelChoiceField(empty_label=None,queryset=Libro.objects.none(),
		help_text='Seleccione un libro para el Bautismo')


	def __init__(self,user, *args, **kwargs):

		super(BautismoFormEditar, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Bautismo',parroquia=parroquia)
      
	
	class Meta():
		model=Bautismo
		fields=('numero_acta','pagina','bautizado','libro','celebrante','fecha_sacramento',
			'lugar_sacramento','padrino','madrina',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')


class EucaristiaForm(ModelForm):
	feligres=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),required=True,
	empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:18/07/2000')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Eucaristia')

	def __init__(self,user, *args, **kwargs):
		
		super(EucaristiaForm, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Eucaristia',parroquia=parroquia)


	class Meta():
		model=Eucaristia
		fields=('numero_acta','pagina','feligres','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante','iglesia')

class EucaristiaFormEditar(ModelForm):
	feligres=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),required=True,
	empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:18/07/2000')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Eucaristia')

	def __init__(self,user, *args, **kwargs):
		
		super(EucaristiaFormEditar, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Eucaristia',parroquia=parroquia)


	class Meta():
		model=Eucaristia
		fields=('numero_acta','pagina','feligres','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante','iglesia')


class ConfirmacionForm(ModelForm):
	confirmado=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),
		required=True,label='Feligres',
	empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:18/07/2000')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	obispo = forms.CharField(required=True,label='Celebrante',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Nombre de Ministro ej: Ob Julio Parrilla')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Confirmacion')

	def __init__(self,user, *args, **kwargs):
		
		super(ConfirmacionForm, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Confirmacion',parroquia=parroquia)


	class Meta():
		model=Confirmacion
		fields=('numero_acta','pagina','confirmado','celebrante','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','iglesia')


class ConfirmacionFormEditar(ModelForm):
	confirmado=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),
		required=True,label='Feligres',
	empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:18/07/2000')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	obispo = forms.CharField(required=True,label='Celebrante',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Nombre de Ministro ej: Ob Julio Parrilla')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Confirmacion')

	def __init__(self,user, *args, **kwargs):
		
		super(ConfirmacionFormEditar, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Confirmacion',parroquia=parroquia)


	class Meta():
		model=Confirmacion
		fields=('numero_acta','pagina','confirmado','libro','fecha_sacramento',
			'lugar_sacramento','celebrante','padrino','madrina','iglesia')


class MatrimonioForm(ModelForm):
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': '','pattern':'[0-9]+'}),
		help_text='Ingrese el numero de pagina ej:5,67')
	novio=forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), 
		required=True, empty_label='--- Seleccione ---', 
		widget=forms.Select(attrs={'required':''}),
		help_text='Presione buscar para encontrar el novio')
	novia=forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), 
		required=True, empty_label='--- Seleccione ---', 
		widget=forms.Select(attrs={'required':''}),
		help_text='Presione buscar para encontrar la novia')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:18/07/2000')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	testigo_novio= forms.CharField(required=True,label='Testigo',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testigo ej: Pablo Robles')
	testigo_novia= forms.CharField(required=True,label='Testiga',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testiga ej:Maria Pincay')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),help_text='Seleccione un libro para el Matrimonio')

	def __init__(self,user, *args, **kwargs):
		
		super(MatrimonioForm, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Matrimonio',parroquia=parroquia)

	class Meta():
		model=Matrimonio
		fields=('numero_acta','pagina','libro','fecha_sacramento','lugar_sacramento','celebrante',
			'padrino','madrina','iglesia','novio','novia','testigo_novio','testigo_novia')

class MatrimonioFormEditar(ModelForm):
	pagina=forms.IntegerField(required=True, label='Pagina', 
		widget=forms.TextInput(attrs={'required': '','pattern':'[0-9]+'}),
		help_text='Ingrese el numero de pagina ej:5,67')
	novio=forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), 
		required=True, empty_label='--- Seleccione ---', 
		widget=forms.Select(attrs={'required':''}),
		help_text='Presione buscar para encontrar el novio')
	novia=forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), 
		required=True, empty_label='--- Seleccione ---', 
		widget=forms.Select(attrs={'required':''}),
		help_text='Presione buscar para encontrar la novia')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	fecha_sacramento = forms.CharField(required=True,label='Fecha de Sacramento',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}),help_text='Seleccione una fecha ej:18/07/2000')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	testigo_novio= forms.CharField(required=True,label='Testigo',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testigo ej: Pablo Robles')
	testigo_novia= forms.CharField(required=True,label='Testiga',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testiga ej:Maria Pincay')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),help_text='Seleccione un libro para el Matrimonio')

	def __init__(self,user, *args, **kwargs):
		
		super(MatrimonioFormEditar, self).__init__(*args, **kwargs)
		parroquia = AsignacionParroquia.objects.get(
			persona__user=user,estado=True).parroquia
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Matrimonio',parroquia=parroquia)

	class Meta():
		model=Matrimonio
		fields=('numero_acta','pagina','libro','fecha_sacramento','lugar_sacramento','celebrante',
			'padrino','madrina','iglesia','novio','novia','testigo_novio','testigo_novia')


#Forms para Parroquia - Funcionando
class ParroquiaForm(ModelForm):
	class Meta:
		model = Parroquia
		fields = ('nombre',)

#Form para asignar parroquia
class AsignarParroquiaForm(ModelForm):
	persona = forms.ModelChoiceField(label = 'Sacerdote', queryset=PerfilUsuario.objects.sacerdotes()) 
	class Meta:
		model = AsignacionParroquia
		widgets = {
		'inicio': forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'}),
		'fin': forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'}),
		}


#Form para Intenciones de Misa - Funcionando
class IntencionForm(ModelForm):
	# fecha = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
	#  widget=forms.DateTimeInput(attrs={'type':'datetime-local'}),
	#  help_text='Ingrese la fecha de la intencion ej:2010-11-13')

	def clean_fecha(self):
		data = self.cleaned_data['fecha']
		if date.today() > data:
	  		raise forms.ValidationError('Lo siento, no puede usar fechas en el pasado')
	 	return data
	
	class Meta:
		model = Intenciones
		fields = ('intencion', 'oferente', 'ofrenda', 'fecha', 'hora', 'individual')
		widgets = {
			'intencion': forms.TextInput(attrs={'required':'', 'title':'intencion'}),
			'oferente': forms.TextInput(attrs={'required':''}),
			'ofrenda': forms.TextInput(attrs={'required':'',  'pattern':'[0-9]+'}),
			'fecha': forms.TextInput(attrs={'required':'', 'type': 'date'}),
			'hora': forms.TextInput(attrs={'required':'', 'type':'time'}),			
		}
		

# Forms para Notas Marginals

class NotaMarginalForm(ModelForm):
	fecha = forms.CharField(help_text='Seleccione una fecha ej:18/07/2000',
		required=True,label='Fecha',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}))
	descripcion=forms.CharField(required=True,label='Descripcion',
		widget=forms.Textarea(attrs={'required':''}),
		help_text='Ingrese una descripcion ej: saco para casarse')
	class Meta():
		model= NotaMarginal
		fields=('fecha','descripcion')
		

