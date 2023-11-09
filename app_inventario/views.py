from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaccion, Proveedor, SubtipoTransaccion, Existencias, DetalleTransaccion
from app_productos.models import Producto
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def transacciones(request):
    transacciones = Transaccion.objects.all()
    subtipos_entrada = SubtipoTransaccion.objects.filter(tipoTransaccion__nombreTipo='Entradas')
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    detalles = DetalleTransaccion.objects.all()  # Obtener todos los detalles de transacción

    context = {
        'transacciones': transacciones,
        'subtipos_entrada': subtipos_entrada,
        'productos': productos,
        'proveedores': proveedores,
        'detalles': detalles,
    }
    return render(request, 'adminTransacciones.html', context)
@staff_member_required
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
            print(e)
            # Manejar el error si es necesario
    return redirect('adminTransacciones')  # Redirigir en caso de que no sea un método POST
@staff_member_required
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
@staff_member_required
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

@staff_member_required
@require_GET
def detalles_transaccion(request):
    # Realiza la lógica de filtrado que necesitas
    transaccion_id = request.GET.get('transaccion_id')  # Ejemplo de cómo podrías recibir el parámetro

    # Filtra los detalles de la transacción
    detalles = DetalleTransaccion.objects.filter(idTransaccion=transaccion_id)
    
    # Prepara los datos que deseas retornar
    data = {
        'detalles': [{'idDetalle': detalle.idDetalle, 'cantidad': detalle.cantidad, 'subtotal': detalle.precio,
                       'nombreProducto': detalle.idProducto.nombre} for detalle in detalles]
    }

    # Retorna los datos en formato JSON
    return JsonResponse(data)

@staff_member_required
def mostrarInventario(request):
    inventario = Existencias.objects.all()
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()

    context = {
        'existencias': inventario,
        'productos': productos,
        'proveedores': proveedores,
    }
    return render(request, 'inventario.html', context)
@staff_member_required
def agregar_al_carrito(request, producto_id):
    # Obtener el carrito del usuario desde la sesión o crearlo si no existe
    carrito = request.session.get('carrito', [])
    
    # Verificar si el producto ya está en el carrito
    if producto_id not in carrito:
        # Agregar el idProducto del producto al carrito
        carrito.append(producto_id)
        
        # Actualizar el carrito en la sesión
        request.session['carrito'] = carrito
        request.session.modified = True
    # Redireccionar a la página de la tienda o a la página de confirmación
    return redirect('tienda')
@staff_member_required
def carritoCompras(request):
    # Obtener los productos del carrito almacenados en la sesión
    carrito = request.session.get('carrito', [])
    
    # Obtener los detalles de los productos en el carrito
    productos_carrito = Producto.objects.filter(idProducto__in=carrito)
    print(productos_carrito)
    return render(request, 'carrito.html', {'productos_carrito': productos_carrito})

@staff_member_required
def eliminar_del_carrito(request, producto_id):
    if 'carrito' in request.session:
        carrito = request.session['carrito']

        if producto_id in carrito:
            # Encuentra la posición del producto en la lista
            posicion = carrito.index(producto_id)
            # Elimina el producto de la lista utilizando la posición
            del carrito[posicion]
            request.session['carrito'] = carrito

    return redirect('carritoCompras')




