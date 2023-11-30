from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaccion, Proveedor, SubtipoTransaccion, Existencias, DetalleTransaccion
from app_productos.models import Producto, Proveedor
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
            valorTotal=valor_total,
            estado = 'E'
        )
        transaccion.save()

        # Captura los detalles de la entrada (puedes tener múltiples detalles)
        detalle_counter = 1
        while True:
            producto = request.POST.get(f'producto_{detalle_counter}')
            print(producto)
            if producto is None:
                break
            cantidad = request.POST.get(f'cantidad_{detalle_counter}')
            precioUnidad = request.POST.get(f'precio_unidad_{detalle_counter}')
            fechaVencimiento = request.POST.get(f'fecha_{detalle_counter}')
            precioDetalle = request.POST.get(f'total_{detalle_counter}')

            # Crea un registro en la tabla DetalleTransaccion
            detalle = DetalleTransaccion(
                idTransaccion=transaccion,
                idProducto_id=producto,
                cantidad=cantidad,
                precioUnidad=precioUnidad,
                fechaVencimiento=fechaVencimiento,
                precio=precioDetalle
            )
            detalle.save()

            # Crea un nuevo registro en la tabla Existencias
            existencia = Existencias(
                idProducto_id=producto,
                cantidad=cantidad,
                fechaLlegada=fechaEntrada,
                fechaVencimiento=fechaVencimiento
            )
            existencia.save()

            detalle_counter += 1
            print(f"Detalle ID: {detalle.idProducto_id}")
            print(f"Existencia ID: {existencia.idProducto_id}")
        return redirect('adminTransacciones')  # Redirige a una vista de éxito
    return render(request, 'adminTransacciones.html')

@staff_member_required
@require_GET
def detalles_transaccion(request):
    # Recibe el id del producto
    transaccion_id = request.GET.get('transaccion_id')  

    # Filtra los detalles de la transacción
    detalles = DetalleTransaccion.objects.filter(idTransaccion=transaccion_id)
    
    # Prepara los datos que deseas retornar
    data = {
        'detalles': [{'idDetalle': detalle.idDetalle, 'precioUnidad': detalle.precioUnidad,'fechaVencimiento': detalle.fechaVencimiento,'cantidad': detalle.cantidad, 'subtotal': detalle.precio,
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
    #for existencia in inventario:
    #    print(f"ID: {existencia.idExistencia}, Producto: {existencia.idProducto}, Cantidad: {existencia.cantidad}, Fecha Llegada: {existencia.fechaLlegada}, Fecha Vencimiento: {existencia.fechaVencimiento}")
    return render(request, 'inventario.html', context)

def agregar_al_carrito(request, producto_id):
    # Obtener el carrito del usuario desde la sesión o crearlo si no existe
    carrito = request.session.get('carrito', [])
    
    # Verificar si el producto ya está en el carrito
    producto_en_carrito = next((item for item in carrito if item['idProducto'] == producto_id), None)
    
    if producto_en_carrito is None:
        # Obtener el producto desde la base de datos (reemplaza esto con tu lógica)
        producto = Producto.objects.get(idProducto=producto_id)
       

        # Agregar el producto al carrito con cantidad inicial 1 y calcular el subtotal
        carrito.append({
            'idProducto': producto_id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad':1,
            'subtotal':producto.precio,
        })
    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    request.session.modified = True

    # Redireccionar a la página de la tienda o a la página de confirmación
    return redirect('tienda')

def carritoCompras(request):
    # Obtener los productos del carrito almacenados en la sesión
    carrito = request.session.get('carrito', [])
        
    # Obtener los detalles de los productos en el carrito
    productos_carrito = carrito
    print(productos_carrito)
    return render(request, 'carrito.html', {'productos_carrito': productos_carrito})

def eliminar_del_carrito(request, producto_id):
    if 'carrito' in request.session:
        carrito = request.session['carrito']

        # Utiliza una estructura de bucle para buscar el producto y eliminarlo
        for item in carrito:
            if item['idProducto'] == producto_id:
                carrito.remove(item)
                break  # Rompe el bucle después de eliminar el primer producto

        request.session['carrito'] = carrito
        request.session.modified = True
        print("se imprime desde eliminar")
        print(carrito)

    return redirect('carritoCompras')

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@require_POST
def actualizar_carrito(request):
    # Asegúrate de manejar el contenido como JSON
    try:
        carrito_data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': 'Error al decodificar JSON'})
    
    # Extrae los productos en una variable auxiliar
    productosRecibidos = carrito_data.get('productos', [])
    print('Porductos en data', carrito_data.get('productos', []))
    print('Porductos recibidos', productosRecibidos)

    carrito = request.session['carrito']
    print('Carrito session antes', carrito)
    # Ahora, carrito_data contendrá la información enviada desde el cliente

    for producto_data in productosRecibidos:
        producto_id = producto_data.get('idProducto')  # Asegúrate de usar el mismo campo
        cantidad_nueva = producto_data.get('cantidad')
        subtotal_nuevo = producto_data.get('subtotal')
        print(producto_id)

        # Busca el producto en el carrito
        for producto_en_carrito in carrito:
            if producto_en_carrito.get('idProducto') == producto_id:
                print(producto_en_carrito['idProducto'])
                # Compara y actualiza la cantidad y el subtotal si es necesario
                if cantidad_nueva != producto_en_carrito.get('cantidad') or subtotal_nuevo != producto_en_carrito.get('subtotal'):
                    producto_en_carrito['cantidad'] = cantidad_nueva
                    producto_en_carrito['subtotal'] = subtotal_nuevo
                break  # No es necesario seguir buscando el mismo producto

    # Actualiza el carrito en la sesión
    request.session['carrito'] = carrito
    request.session.modified = True

    # Realiza las acciones necesarias con los datos del carrito
    # Puedes acceder a los datos con carrito_data['carrito_data']

    # Por ejemplo, imprime los datos recibidos en la consola
    print('Carrito session despues', carrito)
    print('Datos del carrito recibidos:', carrito_data)

    # Retorna una respuesta JSON indicando que la actualización fue exitosa
    return JsonResponse({'status': 'success'})
