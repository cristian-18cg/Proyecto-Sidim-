from django.shortcuts import render, redirect
from .models import Producto, CategoriaProducto
from django.core.paginator import Paginator, Page


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

def tienda(request):
    productos = Producto.objects.all().order_by('idProducto')
    paginator = Paginator(productos, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    print(page)
    context = {'page': page}

    return render(request, 'tienda.html', context)
  