from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models  import User
from django.contrib.auth import login
from django.db import IntegrityError
from .form import UsuariosCreationForm


# Create your views here.



def home(request):
   
    return render(request,'home.html')

def singup(request):       #registro de usuario    
 
    if request.method == 'POST':
        form = UsuariosCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('singup')  # Reemplaza 'ruta_de_redireccion' con la URL a la que quieres redirigir después del registro exitoso
    else:
        form = UsuariosCreationForm()
    return render(request, 'singup.html', {'form': form})

    # if request.method == 'GET':
    #     print ('enviando formulario')
    #     form = UsuariosCreationForm()
    #     return render(request,'singup.html',{
    #     'form':form
    #     })
    # else:
    #     if request.POST['password1'] == request.POST['password2']: #valida que sean iguales las contraseñas
    #         #Registrar usuario
    #         try:
    #          user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1']) #crea el objeto con el usuario a crear
    #          user.save() #guarda usuario
    #          login(request, user) #crea la sesion del usuario la cookies 
    #          print('Registrado')
    #          return redirect('tasks')  #redirecciona    
    #         except IntegrityError:  ##excepcion de usuario UNIQUE en la base de datos 
    #          return render(request,'singup.html',{
    #          'form':UsuariosCreationForm,
    #          'error':'Usuario ya existe'
    #           })   
    #     return render(request,'singup.html',{
    #          'form':UserCreationForm,
    #          'error':'Contraseñas no coinciden'
    #           }) 
