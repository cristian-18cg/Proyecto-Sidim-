from django import forms
from django.core.validators import MaxLengthValidator 
from .models import Usuarios



#Formulario para el registro
class UsuariosCreationForm(forms.ModelForm):
    confirmar_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'idusuario','correo', 'telefono', 'direccion','password']
        labels = {
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'idusuario': 'Documento de identificacion',
            'correo': 'Correo electrónico',
            'password': 'Contraseña',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        widgets = {
            'idusuario': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digita tu cedula 10 numeros'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Andres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Perez'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'ejemplo@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': '3105891457'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'cra 102a# 132-30'}),
        }
    def clean_confirmar_password(self):
        password = self.cleaned_data.get('password')
        confirmar_password = self.cleaned_data.get('confirmar_password')

        if password and confirmar_password and password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return confirmar_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['telefono'].validators.append(MaxLengthValidator(limit_value=10, message='El número de telefono debe tener máximo 10 dígitos.'))
#Formulario para el login
class LoginForm(forms.Form):
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))     