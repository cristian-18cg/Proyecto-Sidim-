from django.db import models

class CategoriaProducto(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.Nombre

    class Meta:
        verbose_name_plural = "Categorías de Productos"

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    imagen_producto = models.ImageField(upload_to='productos/', blank=True, null=True)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productos"     

