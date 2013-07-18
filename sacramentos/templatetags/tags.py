from django import template
from sacramentos.views import padre_create_view
from sacramentos.forms import UsuarioForm, PadreForm
register = template.Library()

@register.inclusion_tag('usuario/padre_form.html', takes_context=True)
def padre(context):
	perfil_padre_form = PadreForm
	usuario_form = UsuarioForm
	ctx = {'perfil_padre_form':perfil_padre_form,'usuario_form':usuario_form}
	return ctx