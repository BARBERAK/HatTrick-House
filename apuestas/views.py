from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import CustomUserCreationForm
from .services import execute_update_api
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def home(request):
    """Home page view."""
    return render(request, 'apuestas/home.html')

class GameListView(ListView):
    model = Game
    template_name = 'apuestas/game_list.html'
    context_object_name = 'games'
    
def create_update(request):
    execute_update_api()
    
    return HttpResponse("""
        <h1>¡Actualización completada!</h1>
        <p>Los partidos y cuotas se han guardado en la base de datos.</p>
        <a href='/'>Volver al inicio</a>
    """)
    
def partidos_liga(request, nombre_liga, categoria):
    dict_ligas = {
        "La Liga - Spain" : "La Liga",
        "premier_league" : "Premier League",
        "champions_league" : "Champions League",
        "NBA" : "NBA",
    }
    
    termino_busqueda = dict_ligas.get(nombre_liga, nombre_liga)
    
    partidos_filtrados = Game.objects.filter(league__icontains=termino_busqueda)
    context = {
        'liga_seleccionada' : nombre_liga.upper(),
        'categoria' : categoria,
        'partidos' : partidos_filtrados
    }
    
    return render(request, 'apuestas/partidos_liga.html' , context=context)

@login_required
def ingresar(request):
    return render(request, 'apuestas/deposit.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # guardamos usuario a la BD automaticamente
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Cuenta {username} creada correctamente!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form' : form})
            
