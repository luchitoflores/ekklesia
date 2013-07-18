from django.conf.urls import include, patterns, url

from .views import usuarioCreateView,UsuarioListView,LibroListView,LibroCreateView,LibroUpdateView
from .views import (
	usuarioCreateView, padre_create_view, 
	LibroCreateView, LibroUpdateView ,LibroListView
	)
urlpatterns = patterns('', 
	url(r'^usuario/$', UsuarioListView.as_view(), name='usuario_list'),


	#urls de usuarios

	url(r'^usuario/add/$', usuarioCreateView, name='usuario_create'),
	url(r'^padre/add/$', padre_create_view, name='padre_create'),
	# urls de libro
	url(r'^libro/$',LibroListView.as_view(),name='libro_list'),
	url(r'^libro/add/$',LibroCreateView.as_view(), name='libro_create'),
	url(r'^libro/(?P<pk>\d+)/$',LibroUpdateView.as_view(), name='libro_update'),


	)