from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import (
	Provincia,Canton,Parroquia
	)


class ProvinciaCreateRead(ListCreateAPIView):
	model = Provincia

class ProvinciaCreateReadUpdateDelete(ListCreateAPIView):
	model =Provincia

class CantonCreateRead(ListCreateAPIView):
	model = Canton

class CantonCreateReadUpdateDelete(ListCreateAPIView):
	model =Canton

class ParroquiaCreateRead(ListCreateAPIView):
	model = Parroquia

class ParroquiaCreateReadUpdateDelete(ListCreateAPIView):
	model =Parroquia


def actualizar_ciudades_elegidas(reuqest):
	if request.is_ajax():
		if request.method == 'GET':
			if request.GET.get('provincia'):
				pass

			if request.GET.get('canton'):
				pass


	