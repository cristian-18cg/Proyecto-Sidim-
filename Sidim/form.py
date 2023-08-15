from django import forms
from .models import Usuarios

class UsuariosCreationForm(forms.ModelForm):
    confirmar_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'idusuario','correo', 'telefono', 'direccion','password']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'idusuario': 'Documento',
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
            'direccion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'cra 102a # 132 -3 0'}),
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
    

class LoginForm(forms.Form):
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))     