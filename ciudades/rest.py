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


	