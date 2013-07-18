from django.conf.urls import include, patterns, url
from .views import usuarioCreateView, padre_create_view

urlpatterns = patterns('', 
	url(r'^usuario/add/$', usuarioCreateView, name='usuario_create'),
	url(r'^padre/add/$', padre_create_view, name='padre_create'),
	)