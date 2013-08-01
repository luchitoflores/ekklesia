from django.conf.urls import include, patterns, url

# from sacramentos.rest import api_usuario_list
from .views import (
	usuarioCreateView, UsuarioListView,padre_create_view, feligres_create_view,edit_usuario_view,
	LibroCreateView, LibroUpdateView ,LibroListView,
	MatrimonioCreateView,MatrimonioListView,MatrimonioUpdateView,
	bautismo_update_view, BautismoListView, bautismo_create_view,
	EucaristiaCreateView,EucaristiaUpdateView,EucaristiaListView,
	ConfirmacionCreateView,ConfirmacionUpdateView,ConfirmacionListView,

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
	url(r'^api/asignarpadre/$', 'sacramentos.rest.edit_padre_viewapi', name='api_setear_padre'),
	url(r'^api/padre/add/$', 'sacramentos.rest.padre_create_ajax', name='api_create_padre'),

	# urls de libro
	url(r'^libro/$',LibroListView.as_view(),name='libro_list'),
	url(r'^libro/add/$',LibroCreateView.as_view(), name='libro_create'),
	url(r'^libro/(?P<pk>\d+)/$',LibroUpdateView.as_view(), name='libro_update'),


	#urls de matrimonio
	url(r'^matrimonio/$',MatrimonioListView.as_view(),name='matrimonio_list'),
	url(r'^matrimonio/add/$',MatrimonioCreateView.as_view(), name='matrimonio_create'),
	url(r'^matrimonio/(?P<pk>\d+)/$',MatrimonioUpdateView.as_view(), name='matrimonio_update'),


	#urls de Bautismo
	#url(r'^usuario/(?P<id_fel>\d+)/bautismo/add/$',bautismo_create_view, name='bautismo_create'),
	url(r'^bautismo/$',BautismoListView.as_view(),name='bautismo_list'),
	url(r'^bautismo/add/$',bautismo_create_view, name='bautismo_create'),
	url(r'^bautismo/(?P<pk>\d+)/$',bautismo_update_view, name='bautismo_update'),


	#urls de Eucaristia
	url(r'^eucaristia/$',EucaristiaListView.as_view(),name='eucaristia_list'),
	url(r'^eucaristia/add/$',EucaristiaCreateView.as_view(), name='eucaristia_create'),
	url(r'^eucaristia/(?P<pk>\d+)/$',EucaristiaUpdateView.as_view(), name='eucaristia_update'),


	#urls de Confirmacion
	url(r'^confirmacion/$',ConfirmacionListView.as_view(),name='confirmacion_list'),
	url(r'^confirmacion/add/$',ConfirmacionCreateView.as_view(), name='confirmacion_create'),
	url(r'^confirmacion/(?P<pk>\d+)/$',ConfirmacionUpdateView.as_view(), name='confirmacion_update'),




	)