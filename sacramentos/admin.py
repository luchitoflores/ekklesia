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
)

admin.site.register(PerfilUsuario)
admin.site.register(Libro)
admin.site.register(Bautismo)
admin.site.register(Eucaristia)
admin.site.register(Confirmacion)
admin.site.register(Matrimonio)
admin.site.register(NotaMarginal)
admin.site.register(Intenciones)
admin.site.register(Parroquia)
admin.site.register(Direccion)

