# -*- coding:utf-8 -*-
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

# from sacramentos.rest import api_usuario_list
from .views import (
	usuarioCreateView, UsuarioListView,padre_create_view, 
	feligres_create_view, edit_usuario_view,
	libro_create_view, libro_update_view ,LibroListView,
	matrimonio_create_view,MatrimonioListView,matrimonio_update_view,
	bautismo_update_view, BautismoListView, bautismo_create_view,
	eucaristia_create_view,eucaristia_update_view,EucaristiaListView,
	confirmacion_create_view,confirmacion_update_view,ConfirmacionListView,
	ParroquiaCreateView, ParroquiaListView, ParroquiaUpdateView,
	IntencionCreateView, IntencionListView, IntencionUpdateView,
	)
urlpatterns = patterns('', 
	#urls de usuarios
	url(r'^usuario/$', UsuarioListView.as_view(), name='usuario_list'),
	url(r'^usuario/add/$', usuarioCreateView, name='usuario_create'),
	url(r'^usuario/(?P<pk>\d+)/$', edit_usuario_view, name='usuario_update'),
	url(r'^padre/add/$', padre_create_view, name='padre_create'),

	url(r'^feligres/add/$', feligres_create_view, name='feligres_create'),
	


	#urls del api rest usuarios
	url(r'^api/usuario/$', 'sacramentos.rest.buscar_usuarios', name='api_usuario_list'),
	url(r'^api/asignarpadre/$', 'sacramentos.rest.edit_padre_viewapi', 
		name='api_setear_padre'),

	url(r'^api/padre/add/$', 'sacramentos.rest.padre_create_ajax', 
		name='api_create_padre'),

	# urls de libro
	url(r'^libro/$',LibroListView.as_view(),name='libro_list'),
	url(r'^libro/add/$',libro_create_view, name='libro_create'),
	url(r'^libro/(?P<pk>\d+)/$',libro_update_view, name='libro_update'),

	#urls de sacramentos
	url(r'^sacramentos/$', TemplateView.as_view(template_name='sacramentos.html'), 
		name='sacramentos'),

	#urls de matrimonio
	url(r'^matrimonio/$',MatrimonioListView.as_view(),name='matrimonio_list'),
	url(r'^matrimonio/add/$',matrimonio_create_view, name='matrimonio_create'),
	url(r'^matrimonio/(?P<pk>\d+)/$',matrimonio_update_view, name='matrimonio_update'),

	#urla de Nota Marginal

	url(r'^api/nota/add/$', 'sacramentos.rest.nota_marginal_create_ajax', 
		name='api_create_nota'),

	#urls de Bautismo
	# url(r'^usuario/(?P<id_fel>\d+)/bautismo/add/$',bautismo_create_view, 
	# 	name='bautismo_create'),
	url(r'^bautismo/$',BautismoListView.as_view(),name='bautismo_list'),
	url(r'^bautismo/add/$',bautismo_create_view, name='bautismo_create'),
	url(r'^bautismo/(?P<pk>\d+)/$',bautismo_update_view, name='bautismo_update'),


	#urls de Eucaristia
	url(r'^eucaristia/$',EucaristiaListView.as_view(),name='eucaristia_list'),
	url(r'^eucaristia/add/$','sacramentos.views.eucaristia_create_view',
	 name='eucaristia_create'),
	url(r'^eucaristia/(?P<pk>\d+)/$',eucaristia_update_view, name='eucaristia_update'),


	#urls de Confirmacion
	url(r'^confirmacion/$',ConfirmacionListView.as_view(),name='confirmacion_list'),
	url(r'^confirmacion/add/$',confirmacion_create_view, name='confirmacion_create'),
	url(r'^confirmacion/(?P<pk>\d+)/$',confirmacion_update_view,
	 name='confirmacion_update'),

	#urls de parroquia eclesiástica
	url(r'^parroquia/$', ParroquiaListView.as_view(), name='parroquia_list'),
	url(r'^parroquia/add/$', ParroquiaCreateView.as_view(), name='parroquia_create'),
	url(r'^parroquia/(?P<pk>\d+)/$', ParroquiaUpdateView.as_view(), 
		name='parroquia_update'),

	#urls para intenciones de misa
	url(r'^intencion/$', IntencionListView.as_view(), name='intencion_list'),
	url(r'^intencion/add/$', IntencionCreateView.as_view(), name='intencion_create'),
	url(r'^intencion/(?P<pk>\d+)/$', IntencionUpdateView.as_view(), 
		name='intencion_update'),


	)