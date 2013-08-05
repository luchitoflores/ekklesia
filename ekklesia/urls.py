from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from sacramentos import urls as sacramentos_urls 
from home import urls as home_urls
from usuarios import urls as usuarios_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ekklesia.views.home', name='home'),
    # url(r'^ekklesia/', include('ekklesia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(sacramentos_urls)),
    url(r'^', include(home_urls)),
    url(r'^', include(usuarios_urls)),
)
