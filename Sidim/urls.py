from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name= "home"),
    ##path('home/', views.home, name="home" ),
    path('cerrarsesion/', views.cerrarsesion, name= "cerrarsesion"),
    path('iniciarsesion/', views.iniciarsesion, name= "iniciarsesion"),
    path('perfil/', views.perfil, name='perfil'),
    path('guardar_perfil/', views.guardar_perfil, name='guardar_perfil'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    
] 