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
            'idusuario': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digita tu cedula 10 numeros'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Andres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Perez'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'ejemplo@gmail.com'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': '3105891457'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'cra 102a # 132 -3 0'}),
        }