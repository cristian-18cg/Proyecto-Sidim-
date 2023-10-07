from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

urlpatterns = [
    path('', views.home, name= "home"),
    ##path('home/', views.home, name="home" ),
    path('cerrarsesion/', views.cerrarsesion, name= "cerrarsesion"),
    path('iniciarsesion/', views.iniciarsesion, name= "iniciarsesion"),
    path('perfil/', views.perfil, name='perfil'),
    path('guardar_perfil/', views.guardar_perfil, name='guardar_perfil'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] 