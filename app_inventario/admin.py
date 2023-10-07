from django.contrib import admin
from .models import Proveedor, TipoTransaccion, SubtipoTransaccion, Transaccion, DetalleTransaccion, Existencias

admin.site.register(Proveedor)
admin.site.register(TipoTransaccion)
admin.site.register(SubtipoTransaccion)
admin.site.register(Transaccion)
admin.site.register(DetalleTransaccion)
admin.site.register(Existencias)
