from django.shortcuts import render, redirect
from .models import Transaccion, Proveedor, SubtipoTransaccion, Existencias, DetalleTransaccion
from app_productos.models import Producto

def transacciones(request):
    transacciones = Transaccion.objects.all()
    subtipos_entrada = SubtipoTransaccion.objects.filter(tipoTransaccion__nombreTipo='Entradas')
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()  # Agrega proveedores al contexto
    context = {
    'transacciones': transacciones,
    'subtipos_entrada': subtipos_entrada,
    'productos': productos,
    'proveedores': proveedores,  # Agrega proveedores al contexto
    }
    return render(request, 'adminTransacciones.html', context)

def crear_proveedor(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            nombre_proveedor = request.POST.get('nombreProveedor')
            id_proveedor = request.POST.get('nitProveedor')
            telefono_proveedor = request.POST.get('telefonoProveedor')
            correo_proveedor = request.POST.get('correoProveedor')

            # Crear y guardar el nuevo proveedor
            nuevo_proveedor = Proveedor(
                idProveedor=id_proveedor,
                nombreProveedor=nombre_proveedor,
                emailProveedor=correo_proveedor,
                telefonoProveedor=telefono_proveedor
            )
            print(nuevo_proveedor)
            nuevo_proveedor.save()

            return redirect('adminTransacciones')
        except Exception as e:
            error_message = str(e)
            # Manejar el error si es necesario
    return redirect('adminTransacciones')  # Redirigir en caso de que no sea un método POST

def editar_proveedor(request):
    if request.method == 'POST':
        try:
            id_proveedor = request.POST.get('nitProveedor')
            nombre_proveedor = request.POST.get('nombreProveedor')
            telefono_proveedor = request.POST.get('telefonoProveedor')
            correo_proveedor = request.POST.get('correoProveedor')

            # Busca la instancia de Proveedor por ID
            proveedor = Proveedor.objects.get(idProveedor=id_proveedor)

            # Actualiza los campos del proveedor
            proveedor.idProveedor = id_proveedor
            proveedor.nombreProveedor = nombre_proveedor
            proveedor.emailProveedor= correo_proveedor
            proveedor.telefonoProveedor = telefono_proveedor
            proveedor.save()  # Guarda los cambios en la base de datos

            return redirect('adminTransacciones')

        except Exception as e:
            error_message = str(e)
            # Maneja el mensaje de error aquí si es necesario
    return redirect('adminTransacciones')

def registrar_entrada(request):
    if request.method == 'POST':
        
        # Captura los datos generales de la transacción
        subtipo_id = request.POST['subtipo']  # Obtén el ID del subtipo desde el formulario
        fechaEntrada = request.POST['fechaIngreso']
        idProveedor = request.POST['idProveedor']
        valor_total = request.POST['valor_total']

        # Recupera la instancia de SubtipoTransaccion usando el ID del formulario
        subtipo = SubtipoTransaccion.objects.get(pk=subtipo_id)

        # Crea un registro en la tabla Transacciones
        transaccion = Transaccion(
            subtipo=subtipo,
            fecha=fechaEntrada,
            idProveedor_id=idProveedor,  # Usa _id para asignar el ID directamente
            valorTotal=valor_total
        )
        transaccion.save()

        # Captura los detalles de la entrada (puedes tener múltiples detalles)
        detalle_counter = 1
        while True:
            producto = request.POST.get(f'producto_{detalle_counter}')
            if producto is None:
                break
            cantidad = request.POST.get(f'cantidad_{detalle_counter}')
            fechaVencimiento = request.POST.get(f'fecha_{detalle_counter}')
            precioDetalle = request.POST.get(f'total_{detalle_counter}')

            # Crea un registro en la tabla DetalleTransaccion
            detalle = DetalleTransaccion(
                idTransaccion=transaccion,
                idProducto_id=producto,
                cantidad=cantidad,
                fechaVencimiento=fechaVencimiento,
                precio=precioDetalle
            )
            detalle.save()

            # Crea un nuevo registro en la tabla Existencias
            Existencias.objects.create(
                idProducto_id=producto,
                cantidad=cantidad,
                fechaLlegada=fechaEntrada,
                fechaVencimiento=fechaVencimiento
            )

            detalle_counter += 1

        return redirect('adminTransacciones')  # Redirige a una vista de éxito

    return render(request, 'adminTransacciones.html')


