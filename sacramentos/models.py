from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
	dni = models.CharField(max_length=10)
	padre = models.ForeignKey(User, related_name='Padre', null=True, blank=True)
	madre = models.ForeignKey(User, related_name='Madre', null=True, blank=True)
	fecha_nacimiento = models.DateField()
	lugar_nacimiento = models.CharField(max_length=100)
	sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
	estado_civil = models.CharField(max_length=10, choices=ESTADO_CIVIL_CHOICES, null=True, blank=True)
	profesion = models.CharField(max_length=50, null=True, blank=True)



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



class Bautismo(Sacramento):
	abuelo_paterno = models.CharField(max_length=200) 
	abuela_paterna = models.CharField(max_length=200)
	abuelo_materno = models.CharField(max_length=200)
	abuela_materna = models.CharField(max_length=200)
	vecinos_paternos = models.CharField(max_length=200)
	vecinos_maternos = models.CharField(max_length=200)


class Eucaristia(Sacramento):
	pass

class Confirmacion(Sacramento):
	obispo = models.CharField(max_length=200)

class Matrimonio(Sacramento):
	testigo_novio = models.CharField(max_length=200)
	testigo_novia = models.CharField(max_length=200)

class NotaMarginal(TimeStampedModel):
	fecha = models.DateField()
	descripcion = models.TextField(max_length=300) 
	sacramento = models.ForeignKey('Sacramento')



class Libro(TimeStampedModel):
	TIPO_LIBRO_CHOICES = (
            ('Bautismo','Bautismo'),
            ('Eucaristia','Eucaristia'), 
            ('Confirmacion','Confirmacion'),
            ('Matrimonio','Matrimonio'),
            ('Intenciones','Intenciones')          
    	)

	numero_libro=models.PositiveIntegerField()
	tipo_libro=models.CharField(max_length=200, choices=TIPO_LIBRO_CHOICES)
	fecha_apertura=models.DateField()
	fecha_cierre=models.DateField()
	estado=models.CharField(max_length=200)
	numero_maximo_actas=models.PositiveIntegerField()

class Intenciones(TimeStampedModel):
	intencion = models.CharField(max_length=200)
	fecha_celebracion = models.DateTimeField()
	oferente = models.CharField(max_length=200)
	precio = models.PositiveIntegerField()



class Parroquia(TimeStampedModel):
	nombre=models.CharField(max_length=100)
	direccion=models.ForeignKey('Direccion')

class Direccion(TimeStampedModel):
	nombre=models.CharField(max_length=100)
	provincia=models.CharField(max_length=100)
	canton=models.CharField(max_length=100)
	ciudad=models.CharField(max_length=100)
	telefono=models.CharField(max_length=100)
	celular=models.CharField(max_length=100)