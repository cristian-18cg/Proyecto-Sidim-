from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminTransacciones/',views.transacciones, name= "adminTransacciones"),
    path('registrar_entrada/',views.registrar_entrada, name= "registrar_entrada"),
    path('detalles_transaccion/', views.detalles_transaccion, name='detalles_transaccion'),
    path('inventario/', views.mostrarInventario, name='inventario'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='quitar_del_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carritoCompras/', views.carritoCompras, name='carritoCompras'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)