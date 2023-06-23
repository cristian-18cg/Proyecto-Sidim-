from django import forms
from .models import Usuarios

class UsuariosCreationForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'idusuario','correo', 'telefono', 'direccion','contrasena']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'idusuario': 'Documento',
            'correo': 'Correo electrónico',
            'contrasena': 'Contraseña',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        widgets = {
            'idusuario': forms.TextInput(attrs={'class': 'my-input-class','placeholder': 'Digita tu cedula 10 numeros'}),
            'nombre': forms.TextInput(attrs={'class': 'my-input-class','placeholder': 'Andres'}),
            'apellido': forms.TextInput(attrs={'class': 'my-input-class','placeholder': 'Perez'}),
            'correo': forms.EmailInput(attrs={'class': 'my-input-class','placeholder': 'ejemplo@gmail.com'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'my-input-class'}),
            'telefono': forms.TextInput(attrs={'class': 'my-input-class','placeholder': '3105891457'}),
            'direccion': forms.TextInput(attrs={'class': 'my-input-class','placeholder': 'cra 102a # 132 -3 0'}),
        }