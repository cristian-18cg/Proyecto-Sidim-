from django.contrib import admin
from .models import CategoriaProducto, Producto

admin.site.register(CategoriaProducto)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'descripcion', 'display_imagen')

    def display_imagen(self, obj):
        return obj.imagen_producto.url if obj.imagen_producto else "No image"
    display_imagen.short_description = 'Imagen'

admin.site.register(Producto, ProductoAdmin)