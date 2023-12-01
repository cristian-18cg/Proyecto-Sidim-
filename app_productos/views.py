from django.shortcuts import render, redirect
from .models import Producto, CategoriaProducto, Proveedor
from django.core.paginator import Paginator, Page
from app_inventario.models import Existencias
from django import template
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def productos_y_categorias(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    proveedores = Proveedor.objects.all()
    context = {'productos': productos, 'categorias': categorias, 'proveedores':proveedores}
    return render(request, 'adminProductos.html', context)

@staff_member_required
def crear_categoria(request):
    if request.method == 'POST':
        try:
            nombre_categoria = request.POST.get('nombreCategoria')

            if nombre_categoria.strip():
                nueva_categoria = CategoriaProducto(Nombre=nombre_categoria)
                nueva_categoria.save()
            else:
                raise Exception('El nombre de la categoría no puede estar en blanco.')
        except Exception as e:
            error_message = str(e)
            # Puedes manejar el mensaje de error y validación de campos aquí

    return redirect('adminProductos')

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

        except Exception as e:
            error_message = "Error al crear el proveedor: revisa los campos de nuevo y vuelve a intentar."
            return render(request,"adminProductos.html",{ "error": error_message})
            
    return redirect('adminProductos')  # Redirigir en caso de que no sea un método POST

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

        except Exception as e:
            error_message = f"Error al crear el producto: {str(e)}"
            print(error_message)
    return redirect('adminProductos')

@staff_member_required
def crear_producto(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            nombre_producto = request.POST.get('nombreProducto')
            precio_producto = request.POST.get('precioProducto')
            categoria_id = request.POST.get('categoriaProducto')  # Asumiendo que este es el ID de la categoría
            proveedor_id = request.POST.get('idProveedor') 
            descripcion_producto = request.POST.get('descripcionProducto')

            # Obtener la categoría
            idcategoria = CategoriaProducto.objects.get(idCategoria=categoria_id)

            # Obtener el proveedor
            idproveedor = Proveedor.objects.get(idProveedor=proveedor_id)

            # Crear y guardar el nuevo producto
            nuevo_producto = Producto(
                nombre=nombre_producto,
                precio=precio_producto,
                categoria=idcategoria,
                descripcion=descripcion_producto,
            )
            nuevo_producto.save()
            print(nuevo_producto)
            
            # Asignar el proveedor después de crear el producto
            nuevo_producto.idProveedor = idproveedor
            nuevo_producto.save()

            if 'imagenProducto' in request.FILES:
                imagen = request.FILES['imagenProducto']
                nuevo_producto.imagen_producto = imagen
                nuevo_producto.save()

            return redirect('adminProductos')
        except Exception as e:
            error_message = f"Error al crear el producto: {str(e)}"
            print(error_message)

    return redirect('adminProductos')  # Redirigir en caso de que no sea un método POST

@staff_member_required
def editar_producto(request):
    if request.method == 'POST':
        try:
            id_producto = request.POST.get('idProducto')
            nombre_producto = request.POST.get('nombreProducto')
            id_categoria = request.POST.get('categoriaProducto')  # Obtén el ID de la categoría
            proveedor_id = request.POST.get('idProveedor')  
            descripcion_producto = request.POST.get('descripcionProducto')
            precio_producto = request.POST.get('precioProducto')
            imagen_producto = request.FILES.get('imagenProducto', None)
            print(imagen_producto)
            # Busca la instancia de Producto por ID
            producto = Producto.objects.get(idProducto=id_producto)
            print(producto)
            # Busca la instancia de CategoriaProducto por ID
            categoria_producto = CategoriaProducto.objects.get(idCategoria=id_categoria)

            # Obtener el proveedor
            idproveedor = Proveedor.objects.get(idProveedor=proveedor_id)

            # Actualiza los campos del producto
            producto.nombre = nombre_producto
            producto.categoria = categoria_producto  # Asigna la instancia de CategoriaProducto
            producto.descripcion = descripcion_producto
            producto.precio = precio_producto
            producto.idProveedor = idproveedor
            
            if imagen_producto is not None:
                producto.imagen_producto = imagen_producto
          
            producto.save()

            return redirect('adminProductos')

        except Exception as e:
            error_message = f"Error al editar el producto: {str(e)}"
            print(error_message)
    return redirect('adminProductos')

@staff_member_required
def editar_categoria(request):
    if request.method == 'POST':
        try:
            id_categoria = request.POST.get('idCategoria')
            nombre_categoria = request.POST.get('nombreCategoria')

            # Busca la instancia de Categoria por ID
            categoria = CategoriaProducto.objects.get(idCategoria=id_categoria)

            # Actualiza los campos de la categoria
            categoria.Nombre = nombre_categoria

            categoria.save()  # Guarda los cambios en la base de datos
            return redirect('adminProductos')

        except Exception as e:
            error_message = str(e)
            # Maneja el mensaje de error aquí si es necesario
    return redirect('adminProductos')

def tienda(request):
    # Rangos de precios
    precios = [
        {'nombre': 'Menos de $10.000', 'min': 0, 'max': 10000},
        {'nombre': '$10.000 - $20.000', 'min': 10000, 'max': 20000},
        {'nombre': '$20.000 - $60.000', 'min': 20000, 'max': 60000},
        {'nombre': '$60.000 - $100.000', 'min': 60000, 'max': 100000},
        {'nombre': '> $100.000', 'min': 100000, 'max': 1000000000},
        {'nombre': 'Mostrar todos', 'min': 0, 'max': 999999999999}
    ]

    # Obtenemops los valores de busqueda
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 999999999999)
    busqueda = request.GET.get('busqueda', '')
    categoria_nombre = request.GET.get('categoria', None)


    # Filtramos con las busquedas y producto con existencias
    productos = Producto.objects.filter(
        precio__gte=min_price,
        precio__lte=max_price,
        idProducto__in=Existencias.objects.values('idProducto'),
         # Filtrar por nombre que contiene la cadena de búsqueda
    ).order_by('nombre')

     # Si hay una busqueda en la barra de busqieda
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    # Si filtra por categoria   
    if categoria_nombre:
        productos = productos.filter(categoria__Nombre=categoria_nombre)


    print(f'Min Price: {min_price}, Max Price: {max_price}, Búsqueda: {busqueda}')
    # Número de productos por página
    productos_por_pagina = 12

    # Número de página actual
    page_number = request.GET.get('page', 1)

    # Creamos un objeto Paginator para la paginación
    paginator = Paginator(productos, productos_por_pagina)

    # Obtenemos los productos de la página actual
    page = paginator.get_page(page_number)

    return render(request, 'tienda.html', {'page': page, 'productos': page, 'precios': precios, 'busqueda': busqueda, 'min_price': min_price, 'max_price': max_price, 'categorias': CategoriaProducto.objects.all()})