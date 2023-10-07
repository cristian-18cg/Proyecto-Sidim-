from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminTransacciones/',views.transacciones, name= "adminTransacciones"),
    path('registrar_entrada/',views.registrar_entrada, name= "registrar_entrada"),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('editar_proveedor/', views.editar_proveedor, name='editar_proveedor'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)