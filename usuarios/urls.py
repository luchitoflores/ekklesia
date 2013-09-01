from django.conf.urls import url, patterns
from .views import GroupList, GroupCreate, GroupUpdate
from .views import login, logout, login_view, logout_view, change_password_view, send_email_view

urlpatterns = patterns ('',
	# url(r'^loginajax/$', loginajax_view),
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    # url(r'^login/$', 'login_view'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout_view , name='logout'), 
    url(r'^password_change/$', change_password_view , name='password_change'),
    url(r'^send/email/$', send_email_view , name='send_email'), 
    url(r'^group/add/$', GroupCreate.as_view(), name='group_create'),
    url(r'^group/$', GroupList.as_view(), name='group_list'),
    url(r'^group/(?P<pk>\d+)/$', GroupUpdate.as_view(), name='group_update'),
)