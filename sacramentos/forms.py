# -*- coding:utf-8 -*-
from django.contrib import messages
from datetime import datetime, date
from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.forms.widgets import RadioSelect
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden


from .models import (PerfilUsuario, 
					Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,Bautismo,
					Direccion, Intenciones,NotaMarginal,Parroquia,AsignacionParroquia, PeriodoAsignacionParroquia, )
from .validators import validate_cedula



class DivErrorList(ErrorList):
	def __unicode__(self):
		return self.as_divs()

	def as_divs(self):
		if not self: 
			return u''
		return u'<div class="error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


#forms para manejo de usuarios
class UsuarioForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *', 
		help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	groups = forms.ModelMultipleChoiceField(required=False, queryset= Group.objects.all(),
		help_text = 'Los grupos a los que este usuario pertenece. Un usuario obtendrá'+
		' todos los permisos concedidos a cada uno sus grupos. Ud. puede seleccionar más de una opción.',
		 widget=forms.CheckboxSelectMultiple())
	email = forms.EmailField(label='Email', 
		help_text='Ingrese correo electrónico. Ej: diocesisloja@gmail.com', required=False)
	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email', 'groups')
		

class UsuarioPadreForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *',
	 help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email')

class UsuarioSecretariaForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *',
	 help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	email = forms.EmailField(required=True, label='Email *', 
		help_text='Ingrese su dirección de correo electrónico',
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email')

class UsuarioSacerdoteForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *', 
		help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	groups = forms.ModelMultipleChoiceField(queryset= Group.objects.all().exclude(name='Feligres'),
		help_text = 'Los grupos a los que este usuario pertenece. '+
		'Un usuario obtendrá todos los permisos concedidos a cada uno sus grupos.'+
		' Ud. puede seleccionar más de una opción.', widget=forms.CheckboxSelectMultiple())
	email = forms.EmailField(required=True, label='Email *', 
		help_text='Ingrese el email. Ej: juan_salinas12@gmail.com',
		widget=forms.TextInput(attrs={'required': ''}))
	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email', 'groups')
		

class PerfilUsuarioForm(ModelForm):

	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']
		if nacionalidad == 'EC' and cedula:
			if not cedula.isdigit():
				raise forms.ValidationError('El número de cédula no debe contener letras')
				return cedula
			if len(cedula)!=10:
				raise forms.ValidationError('El número de cédula debe ser de 10 dígitos')
				return cedula
			valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
			suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
			if int(cedula[9]) != 10 - int(str(suma)[-1:]):
				raise forms.ValidationError('El número de cédula no es válido')
				return cedula

		return cedula


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
	
	
	sexo = forms.TypedChoiceField(label=u'Sexo *', help_text='Elija el sexo de la persona. Ej: Masculino', 
		choices=SEXO_CHOICES, required=True, widget=forms.Select(attrs={'required':''}))
	estado_civil = forms.TypedChoiceField(label=u'Estado Civil *', 
		help_text='Elija el estado civil. Ej: Soltero/a', choices=ESTADO_CIVIL_CHOICES, 
		required=True, widget=forms.Select(attrs={'required':''}))

	
	def __init__(self, padre = PerfilUsuario.objects.none() , madre = PerfilUsuario.objects.none(), *args, **kwargs):
		super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
		self.fields['padre']=forms.ModelChoiceField(required=False, queryset=padre, 
			empty_label='-- Seleccione --')
		self.fields['madre']=forms.ModelChoiceField(required=False, queryset=madre, 
			empty_label='-- Seleccione --')

	class Meta():
		model = PerfilUsuario
		fields = ('nacionalidad', 'dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil' ,
			'profesion', 'padre', 'madre', 'celular');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),


			}
		
class PadreForm(ModelForm):
	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data
	ESTADO_CIVIL_CHOICES    = (
		('', '--- Seleccione ---'),
		('s','Soltero/a'),
		('c','Casado/a'),
		('d','Divorciado/a'),
		('v','Viudo/a')
		)
	estado_civil = forms.TypedChoiceField(label=u'Estado Civil *', 
		help_text='Elija el estado civil. Ej: Soltero/a', choices=ESTADO_CIVIL_CHOICES, 
		required=True, widget=forms.Select(attrs={'required':''}))

	lugar_nacimiento = forms.CharField(help_text='Ingrese el lugar de  nacimiento ej: Loja ', 
		required=True,label='Lugar de Nacimiento *',
		widget=forms.TextInput(attrs={'required':''}))
	class Meta(): 
		model = PerfilUsuario
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil',
		 'profesion');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class SecretariaForm(ModelForm):
	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']
		if nacionalidad == 'EC' and cedula:
			if not cedula.isdigit():
				raise forms.ValidationError('El número de cédula no debe contener letras')
				return cedula
			if len(cedula)!=10:
				raise forms.ValidationError('El número de cédula debe ser de 10 dígitos')
				return cedula
			valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
			suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
			if int(cedula[9]) != 10 - int(str(suma)[-1:]):
				raise forms.ValidationError('El número de cédula no es válido')
				return cedula
		return cedula

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
	
	sexo = forms.TypedChoiceField(label=u'Sexo *', help_text='Elija el sexo de la persona. Ej: Masculino', 
		choices=SEXO_CHOICES, required=True, widget=forms.Select(attrs={'required':''}))
	estado_civil = forms.TypedChoiceField(label=u'Estado Civil *', 
		help_text='Elija el estado civil. Ej: Soltero/a', choices=ESTADO_CIVIL_CHOICES, 
		required=True, widget=forms.Select(attrs={'required':''}))

	class Meta():
		model = PerfilUsuario
		fields = ('nacionalidad', 'dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil');
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

	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']
		if nacionalidad == 'EC' and cedula:
			if not cedula.isdigit():
				raise forms.ValidationError('El número de cédula no debe contener letras')
				return cedula
			if len(cedula)!=10:
				raise forms.ValidationError('El número de cédula debe ser de 10 dígitos')
				return cedula
			valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
			suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
			if int(cedula[9]) != 10 - int(str(suma)[-1:]):
				raise forms.ValidationError('El número de cédula no es válido')
				return cedula

		return cedula

	# fecha_nacimiento = forms.CharField(help_text='Ingrese la fecha de nacimiento con formato dd/mm/yyyy', label='Fecha de Nacimiento',
	# 	widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}))
	# lugar_nacimiento = forms.CharField(help_text='Ingrese el lugar de Nacimiento. Ej: Amaluza', label='Lugar de Nacimiento')
	class Meta(): 
		model = PerfilUsuario
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento', 'celular');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			'dni': forms.TextInput(attrs={'required':''}),
			}




# forms para sacramentos

class LibroForm(ModelForm):
	def clean_fecha_apertura(self):
		data = self.cleaned_data['fecha_apertura']
		if data > date.today():
			raise forms.ValidationError('La fecha de apertura no puede ser mayor o menor a la fecha actual')
		return data

	def clean_fecha_cierre(self):
		data = self.cleaned_data['fecha_cierre']
		if (data):
			if data <= date.today() :
				raise forms.ValidationError('La fecha de cierre no puede ser menor o igual a la fecha actual')
			return data
		else:
			return data

	
			

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
	numero_libro=forms.IntegerField(required=True, label='Numero Libro *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese un numero para libro ej:1,35')

	tipo_libro= forms.TypedChoiceField(label=u'Tipo de Libro *', choices=TIPO_LIBRO_CHOICES, 
		required=True, widget=forms.Select(attrs={'required':''}),
		help_text='Seleccione un tipo de libro')

	estado=forms.ChoiceField(required=True,choices=ESTADO_CHOICES,label='Estado *', 
		widget=RadioSelect(attrs={'required':''}))
	# fecha_apertura = forms.CharField(label=u'Fecha de Apertura', initial=date.today(),
	# 	widget=forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 
	# 		'type':'date'}),help_text='Seleccione una fecha ej:17/12/2010')
	# fecha_cierre = forms.CharField(required=False,label=u'Fecha de Cierre', 
	# 	widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'
	# 		}),help_text='Seleccione una fecha ej:17/12/2010')
	
	
	class Meta():
		model=Libro
		fields = ('numero_libro', 'tipo_libro', 'fecha_apertura', 'fecha_cierre', 
			'estado')
		widgets = {
			'fecha_apertura': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'fecha_cierre': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date',
				'label':'Fecha Cierre *'}),
			
			}



class BautismoForm(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data[u'fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha del Bautismo no puede ser mayor a la fecha actual')
		return data
	# bautizado=forms.ModelChoiceField(
	# 	label='Feligres',
	# 	help_text='Presione buscar para encontrar un feligres',
	# 	queryset=PerfilUsuario.objects.none(),	required=True,	empty_label='--- Seleccione ---',
	# 	widget=forms.Select(attrs={'required':''}))
	pagina=forms.IntegerField(required=True,help_text='Ingrese el numero de pagina ej:5,67', 
		label='Pagina *', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(help_text='Ingrese el numero del acta ej:3,25',
		required=True, 
		label='Numero acta *', widget=forms.TextInput(attrs={'required': ''}))
	
	lugar_sacramento = forms.CharField(help_text='Ingrese el lugar del sacramento ej: Loja ', 
		required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(help_text='Ingrese el nombre de la iglesia: San Jose',
		required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}))
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(user__groups__name='Sacerdote', profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(help_text='Seleccione un libro para el Bautismo',
		queryset=Libro.objects.none(),empty_label=None)

	def __init__(self,user, bautizado=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
		*args, **kwargs):

		super(BautismoForm, self).__init__(*args, **kwargs)
		
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Bautismo',parroquia=asignacion.parroquia)
		self.fields['bautizado']=forms.ModelChoiceField(required=True, queryset=bautizado,
			 empty_label='-- Seleccione --',label='Feligres *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Seleccione --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			widget=forms.Select(attrs={'required':''}))

		

		      	
	class Meta():
		model=Bautismo
		fields=('numero_acta','pagina','bautizado','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}

class BautismoFormEditar(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha del Bautismo no puede ser mayor a la fecha actual')
		return data
	# bautizado=forms.ModelChoiceField(
	# 	label='Feligres',
	# 	help_text='Presione buscar para encontrar un feligres',
	# 	queryset=PerfilUsuario.objects.todos(),	required=True,	empty_label='--- Seleccione ---',
	# 	widget=forms.Select(attrs={'required':''}))
	pagina=forms.IntegerField(required=True,help_text='Ingrese el numero de pagina ej:5,67', 
		label='Pagina *', 
		widget=forms.TextInput(attrs={'required': ''}))
	numero_acta=forms.IntegerField(help_text='Ingrese el numero del acta ej:3,25',
		required=True, 
		label='Numero acta *', widget=forms.TextInput(attrs={'required': ''}))
	
	lugar_sacramento = forms.CharField(help_text='Ingrese el lugar del sacramento ej: Loja ', 
		required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(help_text='Ingrese el nombre de la iglesia: San Jose',
		required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}))
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.none(),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(empty_label=None,queryset=Libro.objects.none(),
		help_text='Seleccione un libro para el Bautismo')


	def __init__(self,user,bautizado=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
	 *args, **kwargs):

		super(BautismoFormEditar, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Bautismo',parroquia=asignacion.parroquia)
		self.fields['bautizado']=forms.ModelChoiceField(required=True, queryset=bautizado,
			 empty_label=None,label='Feligres *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))
			 

      
	
	class Meta():
		model=Bautismo
		fields=('numero_acta','pagina','bautizado','libro','celebrante','fecha_sacramento',
			'lugar_sacramento','padrino','madrina',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class EucaristiaForm(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha de la Eucaristia no puede ser mayor a la fecha actual')
		return data
	# feligres=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),required=True,
	# empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	# help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero acta *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Eucaristia')

	def __init__(self,user, feligres=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
		*args, **kwargs):
		
		super(EucaristiaForm, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Eucaristia',parroquia=asignacion.parroquia)
		self.fields['feligres']=forms.ModelChoiceField(required=True, queryset=feligres,
			 empty_label='--Seleccione --',label='Feligres *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Seleccione --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Eucaristia
		fields=('numero_acta','pagina','feligres','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}


class EucaristiaFormEditar(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha de la Eucaristia no puede ser mayor a la fecha actual')
		return data
	# feligres=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),required=True,
	# empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	# help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero acta *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Eucaristia')

	def __init__(self,user,feligres=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
	 *args, **kwargs):
		
		super(EucaristiaFormEditar, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Eucaristia',parroquia=asignacion.parroquia)
		self.fields['feligres']=forms.ModelChoiceField(required=True, queryset=feligres,
			 empty_label=None,label='Feligres *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Eucaristia
		fields=('numero_acta','pagina','feligres','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class ConfirmacionForm(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha de la Confirmacion no puede ser mayor a la fecha actual')
		return data
	# confirmado=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),
	# 	required=True,label='Feligres',
	# empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	# help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero acta *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Confirmacion')

	def __init__(self,user, confirmado=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
		*args, **kwargs):
		
		super(ConfirmacionForm, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Confirmacion',parroquia=asignacion.parroquia)
		self.fields['confirmado']=forms.ModelChoiceField(required=True, queryset=confirmado,
			 empty_label='-- Seleccione --',label='Feligres *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Seleccione --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))



	class Meta():
		model=Confirmacion
		fields=('numero_acta','pagina','confirmado','celebrante','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class ConfirmacionFormEditar(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha de la Confirmacion no puede ser mayor a la fecha actual')
		return data
	# confirmado=forms.ModelChoiceField(queryset=PerfilUsuario.objects.todos(),
	# 	required=True,label='Feligres',
	# empty_label='--- Seleccione ---',widget=forms.Select(attrs={'required':''}),
	# help_text='Presione buscar para encontrar al feligres')
	pagina=forms.IntegerField(required=True, label='Pagina *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero de pagina ej:5,67')
	numero_acta=forms.IntegerField(required=True, label='Numero acta *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Confirmacion')

	def __init__(self,user, confirmado=PerfilUsuario.objects.none(),
		celebrante=PerfilUsuario.objects.none(),*args, **kwargs):
		
		super(ConfirmacionFormEditar, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Confirmacion',parroquia=asignacion.parroquia)
		self.fields['confirmado']=forms.ModelChoiceField(required=True, queryset=confirmado,
			 empty_label=None,label='Feligres *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Confirmacion
		fields=('numero_acta','pagina','confirmado','libro','fecha_sacramento',
			'lugar_sacramento','celebrante','padrino','madrina','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class MatrimonioForm(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha del Matrimonio no puede ser mayor a la fecha actual')
		return data

	TIPO_MATRIMONIO_CHOICES=(
		('', '--- Seleccione ---'),
        ('Catolico','Catolico'),
        ('Mixto','Mixto'),
        )
	pagina=forms.IntegerField(required=True, label='Pagina *', 
		widget=forms.TextInput(attrs={'required': '','pattern':'[0-9]+'}),
		help_text='Ingrese el numero de pagina ej:5,67')
	# novio=forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), 
	# 	required=True, empty_label='--- Seleccione ---', 
	# 	widget=forms.Select(attrs={'required':''}),
	# 	help_text='Presione buscar para encontrar el novio')
	# novia=forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), 
	# 	required=True, empty_label='--- Seleccione ---', 
	# 	widget=forms.Select(attrs={'required':''}),
	# 	help_text='Presione buscar para encontrar la novia')
	numero_acta=forms.IntegerField(required=True, label='Numero Acta *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	tipo_matrimonio = forms.TypedChoiceField(label=u'Tipo Matrimonio *', 
		help_text='Elija tipo de matrimonio Ej: Catolico o Mixto', 
		choices=TIPO_MATRIMONIO_CHOICES, required=True, 
		widget=forms.Select(attrs={'required':''}))

	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	testigo_novio= forms.CharField(required=True,label='Testigo *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testigo ej: Pablo Robles')
	testigo_novia= forms.CharField(required=True,label='Testiga *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testiga ej:Maria Pincay')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),help_text='Seleccione un libro para el Matrimonio')


	def __init__(self,user,novio=PerfilUsuario.objects.none(),novia=PerfilUsuario.objects.none(),
	celebrante=PerfilUsuario.objects.none(), *args, **kwargs):
		
		super(MatrimonioForm, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Matrimonio',parroquia=asignacion.parroquia)
		self.fields['novio']=forms.ModelChoiceField(required=True, queryset=novio, 
			empty_label='-- Seleccione --',label='Novio *',
			 help_text='Presione buscar para encontrar un novio',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['novia']=forms.ModelChoiceField(required=True, queryset=novia, 
			empty_label='-- Seleccione --',label='Novia *',
			 help_text='Presione buscar para encontrar una novia',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante'] = forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Seleccione --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))

	class Meta():
		model=Matrimonio
		fields=('numero_acta','pagina','libro','fecha_sacramento','lugar_sacramento','celebrante',
			'padrino','madrina','iglesia','novio','novia','testigo_novio','testigo_novia',
			'tipo_matrimonio')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}


class MatrimonioFormEditar(ModelForm):
	def clean_fecha_sacramento(self):
		data = self.cleaned_data['fecha_sacramento']
		if data > date.today():
			raise forms.ValidationError('La fecha del Matrimonio no puede ser mayor a la fecha actual')
		return data
	TIPO_MATRIMONIO_CHOICES=(
		('', '--- Seleccione ---'),
        ('Catolico','Catolico'),
        ('Mixto','Mixto'),
        )
	pagina=forms.IntegerField(required=True, label='Pagina *', 
		widget=forms.TextInput(attrs={'required': '','pattern':'[0-9]+'}),
		help_text='Ingrese el numero de pagina ej:5,67')
	# novio=forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), 
	# 	required=True, empty_label='--- Seleccione ---', 
	# 	widget=forms.Select(attrs={'required':''}),
	# 	help_text='Presione buscar para encontrar el novio')
	# novia=forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), 
	# 	required=True, empty_label='--- Seleccione ---', 
	# 	widget=forms.Select(attrs={'required':''}),
	# 	help_text='Presione buscar para encontrar la novia')
	numero_acta=forms.IntegerField(required=True, label='Numero acta *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese el numero del acta ej:3,25')
	tipo_matrimonio = forms.TypedChoiceField(label=u'Tipo Matrimonio *', 
		help_text='Elija tipo de matrimonio Ej: Catolico o Mixto', 
		choices=TIPO_MATRIMONIO_CHOICES, required=True, 
		widget=forms.Select(attrs={'required':''}))
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	testigo_novio= forms.CharField(required=True,label='Testigo *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testigo ej: Pablo Robles')
	testigo_novia= forms.CharField(required=True,label='Testiga *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testiga ej:Maria Pincay')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),help_text='Seleccione un libro para el Matrimonio')

	def __init__(self,user,novio=PerfilUsuario.objects.none(),novia=PerfilUsuario.objects.none(), 
		celebrante=PerfilUsuario.objects.none(),*args, **kwargs):
		
		super(MatrimonioFormEditar, self).__init__(*args, **kwargs)
		asignacion = AsignacionParroquia.objects.get(
			persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Matrimonio',parroquia=asignacion.parroquia)
		self.fields['novio']=forms.ModelChoiceField(required=False, queryset=novio, 
			empty_label=None,label='Novio *',
			 help_text='Presione buscar para encontrar un novio',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['novia']=forms.ModelChoiceField(required=False, queryset=novia, 
			empty_label=None,label='Novia *',
			 help_text='Presione buscar para encontrar una novia',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Matrimonio
		fields=('numero_acta','pagina','libro','fecha_sacramento','lugar_sacramento','celebrante',
			'padrino','madrina','iglesia','novio','novia','testigo_novio','testigo_novia',
			'tipo_matrimonio')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}


# Forms para Notas Marginals
class NotaMarginalForm(ModelForm):
	def clean_fecha(self):
		data = self.cleaned_data['fecha']
		if data > date.today() or data<date.today():
			raise forms.ValidationError('La fecha no puede ser mayor o menor a la fecha actual')
		return data

	descripcion=forms.CharField(required=True,label='Descripcion *',
		widget=forms.Textarea(attrs={'required':''}),
		help_text='Ingrese una descripcion ej: di copia para matrimonio')
	class Meta():
		model= NotaMarginal
		fields=('fecha','descripcion')
		widgets = {
		'fecha': forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'})
		
		}


#Forms para Parroquia - Funcionando
class ParroquiaForm(ModelForm):
	nombre=forms.CharField(required=True,label='Nombre de parroquia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese nombre de la parroquia ej: El Sagrario')
	class Meta:
		model = Parroquia
		fields = ('nombre',)

#Form para asignar parroquia
class AsignarParroquiaForm(ModelForm):
	persona = forms.ModelChoiceField(label = 'Sacerdote', queryset=PerfilUsuario.objects.sacerdote()) 
	

	def __init__(self, parroquia = Parroquia.objects.all(), *args, **kwargs):
		super(AsignarParroquiaForm, self).__init__(*args, **kwargs)
		self.fields['parroquia']=forms.ModelChoiceField(required=True, queryset=parroquia, 
			empty_label='-- Seleccione --')

	class Meta:
		model = AsignacionParroquia
		fields = ('persona', 'parroquia')
			
	def clean(self):
		cleaned_data = super(AsignarParroquiaForm, self).clean()
		persona = cleaned_data.get("persona")
		parroquia = cleaned_data.get("parroquia")
		
		try:
			esta_activo= PeriodoAsignacionParroquia.objects.get(asignacion__persona=persona, 
				asignacion__parroquia=parroquia, estado=True)
			if esta_activo:
				print esta_activo
				msg = u"El sacerdote ya tiene un periodo activo en la parroquia elegida"
				self._errors["persona"] = self.error_class([msg])
		except ObjectDoesNotExist:
			esta_activo_otra_parroquia= PeriodoAsignacionParroquia.objects.filter(
				asignacion__persona=persona, estado=True).exclude(asignacion__parroquia=parroquia)
			if esta_activo_otra_parroquia:
				msg = u"El sacerdote ya tiene una asignación activa en otra parroquia"
				self._errors["persona"] = self.error_class([msg])
     
		periodo_activo_otra_parroquia= PeriodoAsignacionParroquia.objects.filter(asignacion__parroquia=parroquia, estado=True).exclude(asignacion__persona=persona)
		if periodo_activo_otra_parroquia:
			msg = u"La parroquia elegida ya tiene asignado un párroco con estado activo"
			self._errors["parroquia"] = self.error_class([msg])
		return cleaned_data

#Form para asignar una secretaria a una parroquia
class AsignarSecretariaForm(ModelForm):
	
	# def clean_persona(self):
	# 	data = self.cleaned_data['persona']
	# 	try: 
	# 		asignacion = AsignacionParroquia.objects.get(persona=data)
			
	# 		if asignacion.id:
	# 			raise forms.ValidationError('el perfil seleccionado ya tiene una asignación activa')
	# 	except ObjectDoesNotExist:
	# 		return data

	# 	return data
	def clean(self):
		cleaned_data = super(AsignarSecretariaForm, self).clean()
		persona = cleaned_data.get("persona")
		parroquia = cleaned_data.get("parroquia")
		print persona

		
		# if not persona.user.email:
		# 	msg = u"La persona elegida no tiene registrado un email, proceda a asignarle uno"
		# 	self._errors["persona"] = self.error_class([msg])

		esta_activo_otra_parroquia= PeriodoAsignacionParroquia.objects.filter(asignacion__persona=persona, estado=True).exclude(asignacion__parroquia=parroquia)
		if esta_activo_otra_parroquia:
			msg = u"La persona elegida ya tiene una asignación activa en otra parroquia"
			self._errors["persona"] = self.error_class([msg])
     
		return cleaned_data


	def __init__(self, user, persona = PerfilUsuario.objects.none(), estado=False, *args, **kwargs):
		super(AsignarSecretariaForm, self).__init__(*args, **kwargs)
		self.fields['persona']=forms.ModelChoiceField(label = 'Secretario/a', queryset=persona, empty_label='-- Seleccione --')
		try:
			parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=user, estado=True).asignacion.parroquia
		except ObjectDoesNotExist:
			raise PermissionDenied

		self.fields['parroquia']=forms.ModelChoiceField(queryset=Parroquia.objects.filter(id=parroquia.id), empty_label='-- Seleccione --')

		self.fields['estado']=forms.BooleanField(label='Está activo?', required=False, initial=estado)
	class Meta:
		model = AsignacionParroquia
		fields = ('persona', 'parroquia')
		


class PeriodoAsignacionParroquiaForm(ModelForm):
	
	def clean(self):
		cleaned_data = super(PeriodoAsignacionParroquiaForm, self).clean()
		inicio = self.cleaned_data.get('inicio')
		fin = self.cleaned_data.get('fin')
		presente = self.cleaned_data.get('presente')
		estado = self.cleaned_data.get('estado')
		print presente

		if inicio < date.today():
			msg = u"La fecha inicial no puede ser menor a la fecha actual"
			self._errors["inicio"] = self.error_class([msg])
		if fin:
			if fin < inicio:
				msg = u"La fecha final no puede ser menor que la fecha inicial"
				self._errors["fin"] = self.error_class([msg])

		# if estado:
			
		# 	msg = u"Ud ya tiene un estado activo en esta parroquia"
		# 	self._errors["fin"] = self.error_class([msg])


		return cleaned_data	


	# def clean_fin(self):
	# 	inicio = clean_inicio(self)
	# 	fin = self.cleaned_data['fin']

	# 	if inicio >= fin:
	# 		raise forms.ValidationError('La fecha final no puede ser menor que la fecha inicial')
	# 	return fin

	class Meta:
		model = PeriodoAsignacionParroquia
		fields = ('inicio', 'fin', 'presente', 'estado')
		widgets = {
		'inicio': forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'}),
		'fin': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}),
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

class ReporteIntencionesForm(forms.Form):
   	TIPO_REPORTE = (
		('', '--- Seleccione ---'),
		('d','Diario'),
		('m','Mensual'),
		('a','Anual'),
	)
   	tipo = forms.TypedChoiceField(label=u'Tipo Reporte *', 
		help_text='Seleccione un tipo de reporte Ej: Diario', choices=TIPO_REPORTE, 
		required=True, widget=forms.Select(attrs={'required':''}))

   	fecha=forms.DateField(help_text='Seleccione una fecha ej:18/07/2000',
		required=True,label='Fecha *',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}))

   	hora=forms.CharField(required=False,help_text='Ingrese una hora ej: 8:00 - 17:00',
    	label='Hora',widget=forms.TextInput(attrs={'type':'time'}))

class ReporteSacramentosAnualForm(forms.Form):
	anio=forms.CharField(help_text='Ingrese un año para generar el reporte',label='Año *',
		widget=forms.TextInput(attrs={'required':''}))

class ReportePermisoForm(forms.Form):
	TIPO_SACRAMENTO = (
		('', '--- Seleccione ---'),
		('Bautismo','Bautismo'),
		('Eucaristia','Eucaristia'),
		('Confirmacion','Confirmacion'),
		('Matrimonio','Matrimonio'),
	)
	# feligres=forms.ModelChoiceField(required=True,empty_label='-- Seleccione --',label='Feligres',
	# 	queryset=PerfilUsuario.objects.feligres(),help_text='Seleccione un Feligres',
	# 	widget=forms.Select(attrs={'required':''}))
   	tipo = forms.TypedChoiceField(label=u'Tipo Sacramento *', 
		help_text='Seleccione un tipo de sacramento', choices=TIPO_SACRAMENTO, 
		required=True, widget=forms.Select(attrs={'required':''}))

   	def __init__(self,feligres = PerfilUsuario.objects.none(), *args, **kwargs):
		super(ReportePermisoForm, self).__init__(*args, **kwargs)
		self.fields['feligres']=forms.ModelChoiceField(label = 'Feligres *', 
			queryset=feligres, empty_label='-- Seleccione --',
			widget=forms.Select(attrs={'required':''}))
		
		
