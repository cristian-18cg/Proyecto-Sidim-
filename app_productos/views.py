from django.shortcuts import render, redirect
from .models import Producto, CategoriaProducto
from django.core.paginator import Paginator, Page
from django import template

def productos_y_categorias(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    context = {'productos': productos, 'categorias': categorias}
    return render(request, 'adminProductos.html', context)

def crear_categoria(request):
    if request.method == 'POST':
        try:
            nombre_categoria = request.POST.get('nameCategory')

            if nombre_categoria.strip():
                nueva_categoria = CategoriaProducto(Nombre=nombre_categoria)
                nueva_categoria.save()
            else:
                raise Exception('El nombre de la categoría no puede estar en blanco.')
        except Exception as e:
            error_message = str(e)
            # Puedes manejar el mensaje de error y validación de campos aquí

    return redirect('adminProductos')

def crear_producto(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            nombre_producto = request.POST.get('nombreProducto')
            precio_producto = request.POST.get('precioProducto')
            categoria_id = request.POST.get('categoriaProducto')  # Asumiendo que este es el ID de la categoría
            descripcion_producto = request.POST.get('descripcionProducto')

            # Obtener la categoría
            idcategoria = CategoriaProducto.objects.get(idCategoria=categoria_id)

            # Crear y guardar el nuevo producto
            
            nuevo_producto = Producto(
                nombre=nombre_producto,
                precio=precio_producto,
                categoria=idcategoria,
                descripcion=descripcion_producto
            )
            nuevo_producto.save()

            if 'imagenProducto' in request.FILES:
                imagen = request.FILES['imagenProducto']
                nuevo_producto.imagen_producto = imagen
                nuevo_producto.save()

            return redirect('adminProductos')
        except Exception as e:
            error_message = str(e)
            # Manejar el error si es necesario

    return redirect('adminProductos')  # Redirigir en caso de que no sea un método POST

def editar_producto(request):
    if request.method == 'POST':
        try:
            id_producto = request.POST.get('idProducto')
            nombre_producto = request.POST.get('nombreProducto')
            id_categoria = request.POST.get('categoriaProducto')  # Obtén el ID de la categoría
            descripcion_producto = request.POST.get('descripcionProducto')
            precio_producto = request.POST.get('precioProducto')

            # Busca la instancia de Producto por ID
            producto = Producto.objects.get(idProducto=id_producto)

            # Busca la instancia de CategoriaProducto por ID
            categoria_producto = CategoriaProducto.objects.get(idCategoria=id_categoria)

            # Actualiza los campos del producto
            producto.nombre = nombre_producto
            producto.categoria = categoria_producto  # Asigna la instancia de CategoriaProducto
            producto.descripcion = descripcion_producto
            producto.precio = precio_producto

            producto.save()  # Guarda los cambios en la base de datos

            return redirect('adminProductos')

        except Exception as e:
            error_message = str(e)
            # Maneja el mensaje de error aquí si es necesario

    return redirect('adminProductos')

def tienda(request):
    precios = [
        {'nombre': 'Menos de $10.000', 'min': 0, 'max': 10000},
        {'nombre': '$10.000 - $20.000', 'min': 10000, 'max': 20000},
        {'nombre': '$20.000 - $60.000', 'min': 20000, 'max': 60000},
        {'nombre': '$60.000 - $100.000', 'min': 60000, 'max': 100000},
        {'nombre': 'más $100.000', 'min': 100000, 'max': 1000000000},
        {'nombre': 'Mostrar todos','min':0,'max':999999999999}
        # Agrega más rangos de precios según sea necesario
    ]
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    # mostramos productos de la tienda 
    if min_price and max_price:
        productos = Producto.objects.filter(precio__gte=min_price, precio__lte=max_price)
    else:
        productos = Producto.objects.all()
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    print(page)
    

    return render(request, 'tienda.html', {'page': page, 'productos': productos, 'precios': precios})
