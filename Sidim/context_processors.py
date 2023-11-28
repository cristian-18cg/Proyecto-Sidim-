from .form import UsuariosCreationForm

def form_registro(request):
    return {'form_registro': UsuariosCreationForm()}