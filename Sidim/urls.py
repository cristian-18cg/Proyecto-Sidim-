from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView,CustomPasswordResetConfirmView,error_404
from django.conf.urls import handler404

handler404 = error_404

urlpatterns = [
    path('', views.home, name= "home"),
    path('cerrarsesion/', views.cerrarsesion, name= "cerrarsesion"),
   # path('iniciarsesion/', views.iniciarsesion, name= "iniciarsesion"),
    path('perfil/', views.perfil, name='perfil'),
    path('guardar_perfil/', views.guardar_perfil, name='guardar_perfil'),
    path('permisos/', views.permisos, name='Permisos'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
]