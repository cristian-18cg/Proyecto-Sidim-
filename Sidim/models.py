# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin,  BaseUserManager

class UsuariosManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico debe ser establecido')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, password=password, **extra_fields)   
    
    def get_by_natural_key(self, correo):
        return self.get(correo=correo)
    
class Usuarios(AbstractUser, PermissionsMixin):
    username=None
    first_name=None
    last_name=None
    email=None

    idusuario = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.EmailField(max_length=45,unique=True)
    password = models.CharField(max_length=128)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)

    objects = UsuariosManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(
        default=False,
        help_text="Designates whether this user has all permissions.",
    )
    


    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['idusuario','nombre', 'apellido', 'telefono', 'direccion']

    

    def __str__(self):
        return self.nombre + ' ' + self.apellido
    class Meta:
        managed = True
        db_table = 'usuarios'
      

# Create your views here.



