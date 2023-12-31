from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminProductos/', views.productos_y_categorias, name= "adminProductos"),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('editar_categoria/', views.editar_categoria, name='editar_categoria'),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('editar_proveedor/', views.editar_proveedor, name='editar_proveedor'),
    path('tienda/', views.tienda, name='tienda'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)