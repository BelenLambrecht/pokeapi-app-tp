# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.services.services import getAllImages



def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
#def home(request):
#    images = []
#    favourite_list = []
#
#    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

from django.shortcuts import render
from .layers.services import services  # O importá según cómo tengas la estructura

def home(request):
    images = services.getAllImages()  # obtiene la lista de cards con borde incluido
    favourite_list = []  # por ahora vacío, si no tenés favoritos implementados

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })



# función utilizada en el buscador.
#def search(request):
#    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
#    if (name != ''):
 #       images = []
 #       favourite_list = []

#       return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
#    else:
#        return redirect('home')


def search(request):
    name = request.POST.get('query', '')

    if name != '':
        images = services.filterByCharacter(name)  # Llama a la lógica de filtrado
        favourite_list = []  # Si ya tenés favoritos implementados, podrías usar services.getAllFavourites(request)

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })
    else:
        return redirect('home')


# función utilizada para filtrar por el tipo del Pokemon
#def filter_by_type(request):
 #   type = request.POST.get('type', '')

#    if type != '':
#        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
#        favourite_list = []

#        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
#    else:
#        return redirect('home')


def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = services.filterByType(type)  # ← Acá se aplica el filtro real
        favourite_list = []  # después podés completar esto si tenés favoritos

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })
    else:
        return redirect('home')

#@login_required
#def saveFavourite(request):
#    pass

from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse

@login_required
def saveFavourite(request):
    print("Ingresando a la función")
    if request.method == 'POST':
        # Supongamos que el formulario envía un campo llamado 'item_id'
        item_id = request.POST.get('item_id')
        name = request.POST.get('name')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        base_experience = request.POST.get('base_experience')
        types = request.POST.getlist('types[]')  # Si es un array en el form
        image = request.POST.get('image')

        # Validación rápida (opcional)
        if not item_id or not name:
            messages.error(request, 'Datos incompletos.')
            return redirect('home')

        #falta validar que no se agreguen pokemones ya en la lista de favoritos 
        

        # Crear el favorito
        favorito= Favourite.objects.create(
            id=item_id,
            name=name,
            height=height,
            weight=weight,
            base_experience=base_experience,
            types=types,
            image=image,
            user=request.user
        )
        
        messages.success(request, 'Favorito guardado con éxito')

    return redirect("home")
    
#HttpResponse le da una respueta al navegador (cliente) para poder visualizar algo que yo le pase entre parentesis

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
#@login_required
#def getAllFavouritesByUser(request):
#    pass

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Favourite  # Asegúrate de importar tu modelo

@login_required
def getAllFavouritesByUser(request):
    favourites = Favourite.objects.filter(user=request.user)  # Filtra los favoritos por el usuario actual
    return render(request, 'favourites.html', {'favourite_list': favourites})  # Renderiza la plantilla con los favoritos

#@login_required
#def deleteFavourite(request):
#    pass
from app.layers.services import services

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id = request.POST.get('id')
        success = services.deleteFavouriteById(fav_id)
        if success:
            messages.success(request, 'Favorito eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el favorito')
    else:
        messages.error(request, 'Método no permitido')
    return redirect('favoritos')
#siempre que se haga un cambio en la base de datos se debe actualizar la interfaz del cliente

#@login_required
#def exit(request):
#    logout(request)
#    return redirect('home')

from django.contrib.auth import logout

@login_required
def exit(request):
    logout(request)
    return redirect('index-page')  # Redirige a la página de inicio

