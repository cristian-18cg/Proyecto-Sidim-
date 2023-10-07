from django.db import models
from Sidim.models import Usuarios
from app_productos.models import Producto

class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nombreProveedor = models.CharField(max_length=45, unique=False)
    emailProveedor = models.EmailField(max_length=45)
    telefonoProveedor = models.CharField(max_length=15)

    def __str__(self):
        return self.nombreProveedor

    class Meta:
        verbose_name_plural = "Proveedores"

from django.db import models

# Modelo para TipoTransaccion (Entrada/Salida)
class TipoTransaccion(models.Model):
    idTipo = models.AutoField(primary_key=True)
    nombreTipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreTipo

    class Meta:
        verbose_name = "Tipo de Transacción"
        verbose_name_plural = "Tipos de Transacción"

# Modelo para SubtipoTransaccion (Compras, Devoluciones, Cancelaciones, Ventas, Vencidos, Daños)
class SubtipoTransaccion(models.Model):
    idSubtipo = models.AutoField(primary_key=True)
    nombreSubtipo = models.CharField(max_length=50)
    tipoTransaccion = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreSubtipo

    class Meta:
        verbose_name = "Subtipo de Transacción"
        verbose_name_plural = "Subtipos de Transacción"

# Modelo para Transaccion
class Transaccion(models.Model):
    idTransaccion = models.AutoField(primary_key=True)
    subtipo = models.ForeignKey(SubtipoTransaccion, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    idUsuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"Transacción #{self.idTransaccion}"

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

class DetalleTransaccion(models.Model):
    idDetalle = models.AutoField(primary_key=True)
    idTransaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fechaVencimiento = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"Detalle #{self.idDetalle} - Transacción #{self.idTransaccion}"

    class Meta:
        verbose_name = "Detalle de Transacción"
        verbose_name_plural = "Detalles de Transacción"

class Existencias(models.Model):
    idExistencia = models.AutoField(primary_key=True)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fechaLlegada = models.DateField()
    fechaVencimiento = models.DateField()

    def __str__(self):
        return f"Existencia #{self.idExistencia} - Producto: {self.idProducto.nombre}"

    class Meta:
        verbose_name = "Existencia"
        verbose_name_plural = "Existencias"

