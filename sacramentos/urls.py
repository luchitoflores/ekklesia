from django.conf.urls import include, patterns, url

# from sacramentos.rest import api_usuario_list
from .views import (
	usuarioCreateView, UsuarioListView,padre_create_view, 
	LibroCreateView, LibroUpdateView ,LibroListView,LibroUpdateView
	)
urlpatterns = patterns('', 
	#urls de usuarios
	url(r'^usuario/$', UsuarioListView.as_view(), name='usuario_list'),
	url(r'^usuario/add/$', usuarioCreateView, name='usuario_create'),
	url(r'^padre/add/$', padre_create_view, name='padre_create'),
	#urls del api rest usuarios
	url(r'^api/usuario/$', 'sacramentos.rest.buscar_usuarios', name='api_usuario_list'),
	# urls de libro
	url(r'^libro/$',LibroListView.as_view(),name='libro_list'),
	url(r'^libro/add/$',LibroCreateView.as_view(), name='libro_create'),
	url(r'^libro/(?P<pk>\d+)/$',LibroUpdateView.as_view(), name='libro_update'),
	)