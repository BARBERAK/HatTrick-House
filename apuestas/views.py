from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView

from .models import Game
from .services import execute_update_api


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
    
def partidos_liga(request, nombre_liga):
    context = {
        'liga_seleccionada' : nombre_liga.upper()
    }
    return render(request, 'apuestas/partidos_liga.html' , context=context)
