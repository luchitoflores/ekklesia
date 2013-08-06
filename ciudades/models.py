# -*- coding:utf-8 -*-
from django.forms.widgets import CheckboxSelectMultiple
from django.db import models

# Create your models here.

class Provincia(models.Model):
	nombre=models.CharField(max_length=30,help_text='Ingrese una Provincia Ej: Loja, El Oro')
	abreviatura=models.CharField(max_length=3,help_text='Ingrese una abreviatura Ej:lo, el,p')


	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return '/ciudades/provincia/%i' %(self.id)


class Canton(models.Model):
	nombre=models.CharField(max_length=30,help_text='Ingrese un Canton Ej: Espíndola, Calvas')
	abreviatura=models.CharField(max_length=3, help_text='Ingrese una abreviatura Ej:lo, Ca, A')
	provincia=models.ForeignKey(Provincia, related_name='provincia')


	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return '/ciudades/canton/%i' %(self.id)

class Parroquia(models.Model):
	nombre=models.CharField(max_length=30,help_text='Ingrese Parroquia Ej: Catamayo, Cariamanga')
	abreviatura=models.CharField(max_length=3, help_text='Ingrese una abreviatura Ej:ca, C-a')
	canton=models.ForeignKey(Canton, related_name='canton')
	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return '/ciudades/parroquia/%i' %(self.id)


class Direccion(models.Model):
	nombre=models.CharField(max_length=200)
	provincia=models.ForeignKey(Provincia)
	canton=models.ForeignKey(Canton)
	parroquia=models.ForeignKey(Parroquia, related_name='parroquia_civil')
	telefono=models.CharField(max_length=10)
	celular=models.CharField(max_length=10)

	def __unicode__(self):
		return self.parroquia

