from django.db import models
from sacramentos.models import *

class LibroManager(models.Manager):
	def get_query_set(self):
		return super(LibroManager, self).get_query_set().filter(parroquia='1')
	
	def libros_por_parroquia(self):
	 	return self.models.objects.filter(parroquia=self)


class ParroquiaManager(models.Manager):
	pass

class PersonaManager(models.Manager):
	def male(self):
		return self.model.objects.filter(sexo='Masculino')

	def female(self):
		return self.model.objects.filter(sexo='Femenino')