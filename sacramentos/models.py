from datetime import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings


from ciudades.models import Direccion 
from sacramentos.managers import LibroManager, PersonaManager,BautismoManager
# Create your models here.

def user_new_unicode(self):
    return self.username if self.get_full_name() == "" else self.get_full_name()

# Replace the __unicode__ method in the User class with out new implementation
User.__unicode__ = user_new_unicode 


class TimeStampedModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Libro(TimeStampedModel):
	TIPO_LIBRO_CHOICES = (
            ('Bautismo','Bautismo'),
            ('Eucaristia','Eucaristia'), 
            ('Confirmacion','Confirmacion'),
            ('Matrimonio','Matrimonio')
                     
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

class PerfilUsuario(TimeStampedModel):
	# p.f00_size
	# p.get_foo_size_display()
	SEXO_CHOICES = (
		('m', 'Masculino'), 
		('f','Femenino')
		)	

	ESTADO_CIVIL_CHOICES = (
		('s','Soltero/a'),
		('c','Casado/a'),
		('d','Divorciado/a'),
		('v','Viudo/a')
		)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Usuario', null=True, blank=True)
	dni = models.CharField(max_length=10, null=True, blank=True)
	padre = models.ForeignKey('PerfilUsuario', related_name='Padre', null=True, blank=True)
	madre = models.ForeignKey('PerfilUsuario', related_name='Madre', null=True, blank=True)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True)
	sexo = models.CharField(max_length=10, choices=SEXO_CHOICES,
		help_text='Elija un sexo')
	estado_civil = models.CharField(max_length=10, choices=ESTADO_CIVIL_CHOICES, null=True, blank=True)
	profesion = models.CharField(max_length=50, null=True, blank=True)

	objects = PersonaManager()


	def __unicode__(self):
		if self.user.first_name == None and self.user.last_name == None:
			return self.user.username 
		else:
			return '%s %s' %(self.user.first_name, self.user.last_name) 

	def get_absolute_url_sacerdote(self):
		return u'/sacerdote/%i' % self.id




class Sacramento(TimeStampedModel):
    TIPO_SACRAMENTO_CHOICES = (
            ('Bautismo','Bautismo'),
            ('Eucaristia','Eucaristia'), 
            ('Confirmacion','Confirmacion'),
            ('Matrimonio','Matrimonio')           
    	)
    numero_acta = models.PositiveIntegerField(help_text='Ingrese el numero de acta ej:3,78')
    pagina = models.PositiveIntegerField(help_text='Numero de pagina ej:1,3')
    tipo_sacramento = models.CharField(max_length=50, 
    	choices=TIPO_SACRAMENTO_CHOICES,help_text='Elija un tipo de sacramento')
    fecha_sacramento = models.DateField(help_text='Elija una fecha ej:dd/mm/yyyy')
    lugar_sacramento = models.CharField(max_length=50,
    	help_text='Ingrese el lugar ej: Loja,San Pedro')
    padrino = models.CharField(max_length= 200,
    	help_text='Ingrese el nombre de padrino ej:Jose Rivera')
    madrina = models.CharField(max_length= 200,
    	help_text='Ingrese el nombre de madrina ej:Luisa Mera')
    iglesia = models.CharField(max_length=50,help_text='Nombre de iglesia ej:Catedral')
    libro=models.ForeignKey(Libro, related_name='Libro',
    	help_text='Seleccione un libro')

    
class Bautismo(Sacramento):
	bautizado=models.OneToOneField(PerfilUsuario, related_name='Bautizado',
		help_text='Seleccione un feligres')
	abuelo_paterno = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuelo paterno ej:Jose Rivera')
	abuela_paterna = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuela paterna ej:Maria Gonzalez')
	abuelo_materno = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuelo materno ej:Jose Gonzalez')
	abuela_materna = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de abuela materna ej: Gloria Correa')
	vecinos_paternos = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de vecinos paternos ej:Jose Rivera')
	vecinos_maternos = models.CharField(max_length=200,null=True,blank=True,
		help_text='Nombre de vecinos maternos ej:Ana Vargas')
	objects=BautismoManager()



	def __unicode__(self):
		return '%s %s' %(self.bautizado.user.first_name,self.bautizado.user.last_name)

	


class Eucaristia(Sacramento):
	feligres=models.OneToOneField(PerfilUsuario, related_name='feligres',
		help_text='Seleccione un feligres')
	
	def __unicode__(self):
		return '%s %s' %(self.feligres.user.first_name,self.feligres.user.last_name)

	

class Confirmacion(Sacramento):
	confirmado=models.OneToOneField(PerfilUsuario, related_name='Confirmado',null=True,
		blank=True,help_text='Seleccione un feligres')
	obispo = models.CharField(max_length=200,
		help_text='Nombre de Ministro ej: Ob Julio Parrilla')

	def __unicode__(self):
		return '%s %s' %(self.confirmado.user.first_name,self.confirmado.user.last_name)


class Matrimonio(Sacramento):
	novio=models.OneToOneField(PerfilUsuario, related_name='Novio',
		help_text='Seleccione un novio')
	novia=models.OneToOneField(PerfilUsuario, related_name='Novia',
		help_text='Seleccione una novia')
	testigo_novio = models.CharField(max_length=200,
		help_text='Nombre de testigo ej: Pablo Robles')
	testigo_novia = models.CharField(max_length=200,
		help_text='Nombre de testiga ej:Fernanda Pincay')
	
		

class NotaMarginal(TimeStampedModel):
	fecha = models.DateField()
	descripcion = models.TextField(max_length=300,
		help_text='Descripcion ej:Saco para casarse') 
	bautismo= models.ForeignKey("Bautismo",related_name='Bautismo',null=True,blank=True)
	matrimonio=models.ForeignKey("Matrimonio",related_name='Matrimonio',null=True,
		blank=True)
	def __unicode__(self):
		return self.descripcion



class Libro(TimeStampedModel):
 	TIPO_LIBRO_CHOICES = (
 		('Bautismo','Bautismo'),
        ('Eucaristia','Eucaristia'), 
        ('Confirmacion','Confirmacion'),
        ('Matrimonio','Matrimonio'),
       )
	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	numero_libro=models.PositiveIntegerField(help_text='Numero de libro ej: 1,7,50')
	tipo_libro=models.CharField(max_length=200, choices=TIPO_LIBRO_CHOICES,
		help_text='Elija tipo de Libro')
	fecha_apertura=models.DateField(help_text='Elija una fecha ej:dd/mm/yyyy')
	fecha_cierre=models.DateField(help_text='Elija una fecha ej:dd/mm/yyyy',null=True,
		blank=True)
	estado=models.CharField(max_length=20,choices=ESTADO_CHOICES,
		help_text='Elija un estado')
	numero_maximo_actas=models.PositiveIntegerField(help_text='Numero maximo de actas ej: 40')
	parroquia = models.ForeignKey('Parroquia',help_text='Seleccione una parroquia')

	objects = LibroManager()

	def fecha_cierre_mayor(self):
		if (self.fecha_apertura < self.fecha_cierre):
			return True
		else:
			return False


	def __unicode__(self):
		return '%d %s' %(self.numero_libro,self.tipo_libro)


	

class Intenciones(TimeStampedModel):
	intencion = models.CharField(max_length=200)
	fecha = models.DateTimeField()
	oferente = models.CharField(max_length=200)
	precio = models.PositiveIntegerField()

	def __unicode__(self):
		return self.intencion

	def get_absolute_url(self):
		return u'/intencion/%i' % self.id


class Parroquia(TimeStampedModel):
	nombre=models.CharField('Nombre de la Parroquia',max_length=100)
	direccion=models.ForeignKey(Direccion, related_name='direccion', verbose_name=u'Prueba')

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
