from django import template
from sacramentos.forms import UsuarioForm, PadreForm,PerfilUsuarioForm
register = template.Library()

@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})
