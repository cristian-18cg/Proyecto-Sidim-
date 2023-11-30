from django import forms
from django.core.validators import MaxLengthValidator 
from .models import Usuarios
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import MinimumLengthValidator

#Enviar correo
class CustomPasswordResetForm(forms.Form):
    
     correo = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email','class': 'form-control','placeholder': 'Correo electrónico'}),
    )
    
     def clean_correo(self):
        correo = self.cleaned_data['correo']
        return correo

     def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',email_template_name='registration/password_reset_email.html', use_https=False,token_generator=default_token_generator, from_email=None, request=None, html_email_template_name=None,extra_email_context=None):

        email = self.cleaned_data['correo']
        
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email = self.cleaned_data["correo"]
        
        send_mail(
            subject_template_name,
            email_template_name,
            extra_email_context,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_email_template_name,
        )


#Asignar nueva contraseña recuperar

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Nueva Contraseña'}),
    )

    new_password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirmar Contraseña'}),
    )
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Validaciones de seguridad
        try:
            MinimumLengthValidator().validate(new_password1)
        except forms.ValidationError as e:
            self.add_error('new_password1', e)

        return cleaned_data

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)




#Formulario para el registro
class UsuariosCreationForm(forms.ModelForm):
    confirmar_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'pattern': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$', 'title': 'La contraseña debe tener al menos una mayúscula, una minúscula, un número y ser de al menos 8 caracteres.'})
    )
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
            'correo': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'ejemplo@ejemplo.com'}),
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
    