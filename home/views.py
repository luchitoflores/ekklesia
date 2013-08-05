# *-* coding:utf-8 *-* 
# Create your views here.
import json

from django.http import HttpResponse, HttpResponseRedirect


def index_view(request):
	return HttpResponseRedirect('/')

def home_view(request):
	return HttpResponseRedirect('/home/')

