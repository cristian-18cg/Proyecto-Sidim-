
class Existencias(models.Model):
    existencia_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha_llegada = models.DateField()
    fecha_vencimiento = models.DateField()

    class Meta:
        managed = True    
        db_table = 'existencias'


class Productos(models.Model):
    producto_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    categoria = models.ForeignKey(CategoriaProducto, models.DO_NOTHING)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'productos'


class Proveedores(models.Model):
    proveedor_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=60)
    teléfono = models.CharField(max_length=15)
    correo = models.CharField(max_length=40)

    class Meta:
        managed = True
        db_table = 'proveedores'


class Tipostransaccion(models.Model):
    tipo_transaccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    categora_transaccion = models.ForeignKey(CategoriaTransaccion, models.DO_NOTHING, db_column='categora_transaccion')

    class Meta:
        managed = True
        db_table = 'tipostransaccion'


class Transacciones(models.Model):
    transaccion_id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Tipostransaccion, models.DO_NOTHING, db_column='tipo')
    fecha = models.DateField()
    responsable = models.ForeignKey(Clientes, models.DO_NOTHING)
    valor_total = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'transacciones'


class CategoriaProducto(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'categoria_producto'


class CategoriaTransaccion(models.Model):
    categoria_transaccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'categoria_transaccion'


class Clientes(models.Model):
    cliente = models.OneToOneField('Usuarios', models.CASCADE, primary_key=True)
    usuario_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'clientes'


class Detallestransacciones(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    transaccion = models.ForeignKey('Transacciones', models.DO_NOTHING, blank=True, null=True)
    producto = models.ForeignKey('Existencias', models.DO_NOTHING, to_field='existencia_id', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'detallestransacciones'