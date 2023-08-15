from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models  import User
from django.contrib.auth import login, logout,authenticate
from django.db import IntegrityError
from .form import UsuariosCreationForm, LoginForm


def home(request):
   try:
     if request.method == 'POST':
          form_registro = UsuariosCreationForm(request.POST)
          if form_registro.is_valid():
               usuario = form_registro.save()
               login(request,usuario)
               return redirect('home')  # Reemplaza 'ruta_de_redireccion' con la URL a la que quieres redirigir después del registro exitoso
     else:
          form_registro = UsuariosCreationForm()       
     return render(request, 'home.html', {'form_registro': form_registro})
   except:
       return render(request, 'home.html', {
            'form_registro': form_registro,
            "error":"Algo salió mal, revisa tus campos."
            })
       


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

  