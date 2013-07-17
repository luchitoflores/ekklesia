from django.conf.urls import include, patterns, url
from .views import usuarioCreateView

urlpatterns = patterns('', 
	url(r'^usuario/add/$', usuarioCreateView, name='usuario_create'),
	)