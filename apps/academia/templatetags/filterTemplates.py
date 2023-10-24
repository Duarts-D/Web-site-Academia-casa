from django.template import Library

register = Library()

@register.filter(name='jsoff')
def verificarCategoriaAtivaJsOff(categoriaPagina,categoriaUrl):
   verificador = bool(str(categoriaPagina) == str(categoriaUrl))
   if verificador:
      return True
   else:
      False