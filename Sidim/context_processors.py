from .form import UsuariosCreationForm

from app_productos.models import CategoriaProducto
def form_registro(request):
    
    return {'form_registro': UsuariosCreationForm()}


def categorias(request):
    categorias = CategoriaProducto.objects.all()[:6]
    return {'categorias': categorias}