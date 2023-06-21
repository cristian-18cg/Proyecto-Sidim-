from django import forms
from .models import Usuarios

class UsuariosCreationForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['idusuario','nombre', 'apellido', 'correo', 'contrasena', 'telefono', 'direccion']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo electrónico',
            'contrasena': 'Contraseña',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'my-input-class'}),
            'apellido': forms.TextInput(attrs={'class': 'my-input-class'}),
            'correo': forms.EmailInput(attrs={'class': 'my-input-class','placeholder': 'ejemplo@gmail.com'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'my-input-class'}),
            'telefono': forms.TextInput(attrs={'class': 'my-input-class'}),
            'direccion': forms.TextInput(attrs={'class': 'my-input-class'}),
        }