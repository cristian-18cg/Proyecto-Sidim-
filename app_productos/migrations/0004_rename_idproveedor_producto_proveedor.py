# Generated by Django 4.2.2 on 2023-12-01 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_productos', '0003_proveedor_producto_idproveedor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='idProveedor',
            new_name='proveedor',
        ),
    ]
