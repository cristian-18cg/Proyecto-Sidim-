from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models  import User
from django.contrib.auth import login, logout
from django.db import IntegrityError
from .form import UsuariosCreationForm


def home(request):
   if request.method == 'POST':
        form = UsuariosCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Reemplaza 'ruta_de_redireccion' con la URL a la que quieres redirigir después del registro exitoso
   else:
        form = UsuariosCreationForm()       
   return render(request, 'home.html', {'form': form})
   

