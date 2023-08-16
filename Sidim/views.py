from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models  import User
from django.contrib.auth import login, logout,authenticate
from django.db import IntegrityError
from .form import UsuariosCreationForm, LoginForm
from .models import Usuarios


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

  