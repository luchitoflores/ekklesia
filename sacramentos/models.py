from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from ciudades.models import Provincia, Canton, Parroquia, Direccion 

# Create your models here.

class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class PerfilUsuario(TimeStampedModel):

	SEXO_CHOICES = (
		('Masculino', 'Masculino'), 
		('Femenino','Femenino')
		)	

	ESTADO_CIVIL_CHOICES    = (
		('Soltero/a','Soltero/a'),
		('Casado/a','Casado/a'),
		('Divorciado/a','Divorciado/a'),
		('Viudo/a','Viudo/a')
		)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Usuario', null=True, blank=True)
	dni = models.CharField(max_length=10, null=True, blank=True)
	padre = models.ForeignKey(User, related_name='Padre', null=True, blank=True)
	madre = models.ForeignKey(User, related_name='Madre', null=True, blank=True)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True)
	sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
	estado_civil = models.CharField(max_length=10, choices=ESTADO_CIVIL_CHOICES, null=True, blank=True)
	profesion = models.CharField(max_length=50, null=True, blank=True)



	def __unicode__(self):
		return '%s %s' %(self.user.first_name, self.user.last_name) 

	# class Meta:
	# 	ordering = ('user__last_name', 'user__first_name')




class Sacramento(TimeStampedModel):
    TIPO_SACRAMENTO_CHOICES = (
            ('Bautismo','Bautismo'),
            ('Eucaristia','Eucaristia'), 
            ('Confirmacion','Confirmacion'),
            ('Matrimonio','Matrimonio')           
    	)

    numero_acta = models.PositiveIntegerField()
    pagina = models.PositiveIntegerField()
   
    tipo_sacramento = models.CharField(max_length=50, choices=TIPO_SACRAMENTO_CHOICES)
    fecha_sacramento = models.DateField()
    lugar_sacramento = models.CharField(max_length=50)
    padrino = models.CharField(max_length= 200)
    madrina = models.CharField(max_length= 200)
    iglesia = models.CharField(max_length=50)
    class Meta:
    	abstract=True



class Bautismo(Sacramento):
	bautizado=models.OneToOneField(PerfilUsuario, related_name='Bautizado',null=True,blank=True)
	abuelo_paterno = models.CharField(max_length=200) 
	abuela_paterna = models.CharField(max_length=200)
	abuelo_materno = models.CharField(max_length=200)
	abuela_materna = models.CharField(max_length=200)
	vecinos_paternos = models.CharField(max_length=200)
	vecinos_maternos = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s %s' %(self.bautizado.user.first_name,self.bautizado.user.last_name)

	


class Eucaristia(Sacramento):
	feligres=models.OneToOneField(PerfilUsuario, related_name='feligres', null=True,blank=True)
	
	def __unicode__(self):
		return '%s %s' %(self.feligres.user.first_name,self.feligres.user.last_name)

	

class Confirmacion(Sacramento):
	confirmado=models.OneToOneField(PerfilUsuario, related_name='Confirmado',null=True,blank=True)
	obispo = models.CharField(max_length=200)

	def __unicode__(self):
		return '%s %s' %(self.confirmado.user.first_name,self.confirmado.user.last_name)


class Matrimonio(Sacramento):
	novio=models.OneToOneField(PerfilUsuario, related_name='Novio',null=True,blank=True)
	novia=models.OneToOneField(PerfilUsuario, related_name='Novia',null=True,blank=True)
	testigo_novio = models.CharField(max_length=200)
	testigo_novia = models.CharField(max_length=200)
	
		

class NotaMarginal(TimeStampedModel):
	fecha = models.DateField()
	descripcion = models.TextField(max_length=300) 
	matrimonio = models.ForeignKey('Matrimonio')
	
	def __unicode__(self):
		return self.descripcion


class Libro(TimeStampedModel):
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
	numero_libro=models.PositiveIntegerField()
	tipo_libro=models.CharField(max_length=200, choices=TIPO_LIBRO_CHOICES)
	fecha_apertura=models.DateField()
	fecha_cierre=models.DateField()
	estado=models.CharField(max_length=20,choices=ESTADO_CHOICES)
	numero_maximo_actas=models.PositiveIntegerField()

	def fecha_cierre_mayor(self):
		if (self.fecha_apertura < self.fecha_cierre):
			return True
		else:
			return False


	def __unicode__(self):
		return '%d %s' %(self.numero_libro,self.tipo_libro)

	

class Intenciones(TimeStampedModel):
	intencion = models.CharField(max_length=200)
	fecha_celebracion = models.DateTimeField()
	oferente = models.CharField(max_length=200)
	precio = models.PositiveIntegerField()

	def __unicode__(self):
		return self.intencion


class Parroquia(TimeStampedModel):
	nombre=models.CharField(max_length=100)
	direccion=models.ForeignKey(Direccion, related_name='direccion')

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return '/parroquia/%s' %(self.id)

# class Direccion(TimeStampedModel):
# 	nombre=models.CharField(max_length=200)
# 	provincia=models.ForeignKey(Provincia)
# 	canton=models.ForeignKey(Canton)
# 	parroquia=models.ForeignKey(Parroquia)
# 	telefono=models.CharField(max_length=10)
# 	celular=models.CharField(max_length=10)

# 	def __unicode__(self):
# 		return self.parroquia
