# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.views.generic import TemplateView
from django.conf import settings
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CategoriaProducto(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria_producto'


class CategoriaTransaccion(models.Model):
    categoria_transaccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria_transaccion'


class Clientes(models.Model):
    cliente = models.OneToOneField('Usuarios', models.DO_NOTHING, primary_key=True)
    usuario_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clientes'


class Detallestransacciones(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    transaccion = models.ForeignKey('Transacciones', models.DO_NOTHING, blank=True, null=True)
    producto = models.ForeignKey('Existencias', models.DO_NOTHING, to_field='existencia_id', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detallestransacciones'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empleados(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'empleados'


class Existencias(models.Model):
    existencia_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha_llegada = models.DateField()
    fecha_vencimiento = models.DateField()

    class Meta:
        managed = False
        db_table = 'existencias'


class Productos(models.Model):
    producto_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    categoria = models.ForeignKey(CategoriaProducto, models.DO_NOTHING)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'productos'


class Proveedores(models.Model):
    proveedor_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=60)
    teléfono = models.CharField(max_length=15)
    correo = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'proveedores'


class Tipostransaccion(models.Model):
    tipo_transaccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    categora_transaccion = models.ForeignKey(CategoriaTransaccion, models.DO_NOTHING, db_column='categora_transaccion')

    class Meta:
        managed = False
        db_table = 'tipostransaccion'


class Transacciones(models.Model):
    transaccion_id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Tipostransaccion, models.DO_NOTHING, db_column='tipo')
    fecha = models.DateField()
    responsable = models.ForeignKey(Clientes, models.DO_NOTHING)
    valor_total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'transacciones'


class Usuarios(models.Model):
    idusuario = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(max_length=45,unique=True)
    contrasena = models.CharField(max_length=15)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)
    USERNAME_FIELD = 'correo'
    class Meta:
        managed = False
        db_table = 'usuarios'

# Create your views here.




class MiVista(TemplateView):
    template_name = 'base.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context
    