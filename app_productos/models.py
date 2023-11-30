from django.db import models

class CategoriaProducto(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.Nombre

    class Meta:
        verbose_name_plural = "Categorías de Productos"
        

class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nombreProveedor = models.CharField(max_length=45, unique=False)
    emailProveedor = models.EmailField(max_length=45)
    telefonoProveedor = models.CharField(max_length=15)

    def __str__(self):
        return self.nombreProveedor

    class Meta:
        verbose_name_plural = "Proveedores"


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True)
    imagen_producto = models.ImageField(upload_to='productos/', blank=True, null=True)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Productos"     

