# -*- coding:utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
PerfilUsuario,
Libro, Bautismo, Eucaristia, Confirmacion, Matrimonio, NotaMarginal,
Intenciones,
Parroquia, Direccion, 
AsignacionParroquia,
PeriodoAsignacionParroquia,
)
# def user_unicode(self):
#    	return  u'%s %s' % (self.first_name, self.last_name)

# User.__unicode__ = user_unicode
# admin.site.unregister(User)
# admin.site.register(User)




admin.site.register(PerfilUsuario)
admin.site.register(Libro)
admin.site.register(Bautismo)
admin.site.register(Eucaristia)
admin.site.register(Confirmacion)
admin.site.register(Matrimonio)
admin.site.register(NotaMarginal)
admin.site.register(Intenciones)
admin.site.register(Parroquia)
admin.site.register(AsignacionParroquia)
admin.site.register(PeriodoAsignacionParroquia)

