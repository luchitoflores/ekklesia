from django import template
from sacramentos.forms import UsuarioForm, PadreForm,PerfilUsuarioForm
register = template.Library()

# @register.inclusion_tag('usuario/form_padre.html', takes_context=True)
# def padre(context):
# 	form_perfil_padre = PadreForm
# 	form_usuario = UsuarioForm
# 	ctx = {'form_perfil_padre':form_perfil_padre,'form_usuario':form_usuario}
# 	return ctx

@register.inclusion_tag('usuario/feligres.html', takes_context=True)
def feligres(context):
	form_perfil = PadreForm()
	form_usuario = UsuarioForm()
	ctx = {'form_padre':form_perfil,'form_usuariopadre':form_usuario}
	return ctx

@register.inclusion_tag('direccion/direccion_form.html', takes_context=True)
def direccion(context):
	pass

