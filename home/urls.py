from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$',TemplateView.as_view(template_name='index.html'), name='index'),
	url(r'^home/$', TemplateView.as_view(template_name='home.html'), name='home'),   
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),  
)