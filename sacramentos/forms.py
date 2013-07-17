from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import PerfilUsuario

class UsuarioForm(ModelForm):
	class Meta:
		model = User
		fields= ('first_name', 'last_name')

class PerfilUsuarioForm(ModelForm):
	class Meta:
		model = PerfilUsuario
		fields = ('dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'profesion');