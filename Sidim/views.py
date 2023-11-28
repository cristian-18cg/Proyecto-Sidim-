from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout,authenticate, update_session_auth_hash
from .form import UsuariosCreationForm, LoginForm, CustomPasswordResetForm,CustomPasswordResetForm, CustomSetPasswordForm
from .models import Usuarios
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy,reverse
from django.views import View
from django.http import HttpRequest
from django.contrib.auth.views import PasswordResetConfirmView

def form_registro(request):
    return {'form_registro': UsuariosCreationForm()}

def home(request):
   
   if request.method == 'POST':
    action = request.POST.get('action')
    
    if action == "register":
        form_registro = UsuariosCreationForm(request.POST)#toma los datos de nuetro form de registro
        if form_registro.is_valid():
            form_registro.save() #guarda el registro nuevo si fue valido
            user = authenticate(request, correo=form_registro.cleaned_data['correo'], password=form_registro.cleaned_data['password']) #inicia la sesion despues del registro exitoso 
            if user is not None:
                login(request, user)# inicia la sesion d
                return render(request, 'home.html', {"registrado_mensaje": "Registro exitoso."}) #redireciona a la pagina que se quiere
            else:
                return render(request, 'home.html', {"error": "Error al autenticar después del registro."})
        else:
            return render(request, 'home.html', {'form_registro': form_registro, "error": "Error en el formulario de registro."})
    elif action == "login":
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        user = authenticate(request, correo=correo, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
           try:
            user = Usuarios.objects.get(correo=correo) #busca el correo ingresado si existe 
            return render(request, 'home.html', {"error": "Credenciales inválidas para el inicio de sesión."})
           except Usuarios.DoesNotExist: 
            return render(request, 'home.html', {"error": "El usuario no existe."})
   else:
    form_registro = UsuariosCreationForm()  # Crea un nuevo formulario en caso de GET

   return render(request, 'home.html', {'form_registro': form_registro})

def cerrarsesion(request):
  logout(request)
  return redirect('home')

def iniciarsesion(request):
 if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            user = authenticate(request, correo=correo, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Cambia 'dashboard' a la URL deseada después de iniciar sesión
 else:
        form = LoginForm()
 return render(request, 'home.html', {'form': form})

@login_required 
def perfil(request):
    # Obtén el usuario logeado actualmente
    logged_in_user = request.user
 
    # Usa el correo electrónico del usuario logeado para obtener sus datos
    user_data = get_object_or_404(Usuarios, correo=logged_in_user.correo)

    context = {
        'user_data': user_data
    }
    return render(request, 'profile.html', context)
@login_required 
def guardar_perfil(request):
    if request.method == 'POST':
        logged_in_user = request.user
        user_data = get_object_or_404(Usuarios, correo=logged_in_user.correo)

        # Obtén los datos enviados desde el formulario
        nombre = request.POST.get('first_name')
        apellido = request.POST.get('last_name')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        # Compara los datos con los datos actuales en la base de datos
        if nombre != user_data.nombre:
            user_data.nombre = nombre
        if apellido != user_data.apellido:
            user_data.apellido = apellido
        if telefono != user_data.telefono:
            user_data.telefono = telefono
        if direccion != user_data.direccion:
            user_data.direccion = direccion


        user_data.save()

        return redirect('perfil')

    return redirect('perfil')
@login_required 
def cambiar_contrasena(request):
    if request.method == 'POST':
        contrasena_actual = request.POST.get('contrasena_actual')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        if request.user.check_password(contrasena_actual) and nueva_contrasena == confirmar_contrasena:
            request.user.set_password(nueva_contrasena)
            request.user.save()

            # Actualizar la sesión de autenticación
            update_session_auth_hash(request, request.user)

            messages.success(request, 'La contraseña ha sido cambiada exitosamente.')
        else:
            messages.error(request, 'Hubo un error al cambiar la contraseña. Asegúrate de ingresar la contraseña actual correctamente y de que las nuevas contraseñas coincidan.')

    return render(request, 'profile.html')


class CustomPasswordResetView(View):
    template_name = 'registration/password_reset_form.html'

    def get(self, request):
        form = CustomPasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']

            # Obtiene el usuario con el correo proporcionado
            User = get_user_model()
            try:
                user = User.objects.get(correo=correo)
            except User.DoesNotExist:
                messages.error(request, 'No hay ninguna cuenta asociada a este correo electrónico.')
                return redirect('password_reset_form')  # Reemplaza con la URL de tu página de error

            # Genera el token de reinicio de contraseña
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construye la URL completa para restablecer la contraseña
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Intenta enviar el correo electrónico
            try:
                send_mail(
                    'Reestablecimiento de contraseña SIDIM',
                    f'Sigue este enlace para restablecer tu contraseña: {reset_url}',
                    'noreply@example.com',
                    [correo],
                    fail_silently=False,
                )
            except BadHeaderError as e:
                messages.error(request, 'Error al construir el encabezado del correo electrónico.')
                return redirect('password_reset_confirm')  # Reemplaza con la URL de tu página de error

            messages.success(request, 'Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.')
            return redirect('password_reset_done')  # Reemplaza con la URL de éxito

        return render(request, self.template_name, {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = CustomSetPasswordForm

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = get_user_model().objects.get(pk=uid)
            return user
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist, UnicodeDecodeError):
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']

        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            kwargs['user'] = user
        else:
            messages.error(self.request, 'El enlace de restablecimiento de contraseña no es válido.')
            return {}

        return kwargs

    def form_valid(self, form):
        # Puedes acceder a los campos específicos de tu modelo de usuario personalizado aquí
        # Ejemplo: form.cleaned_data['user'].nombre
        login(self.request, form.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un problema con el formulario de restablecimiento de contraseña.')
        return redirect('home') 