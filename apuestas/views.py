from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from .models import Game, Bet, UserProfile
from .forms import CustomUserCreationForm
from .services import execute_update_api
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q


def home(request):
    """Home page view."""
    return render(request, 'apuestas/home.html')

class BetListView(LoginRequiredMixin,ListView):
    model = Bet
    template_name = 'apuestas/bet_list.html'
    context_object_name = 'bets'
    
    # Sobrescribimos esta función para filtrar las apuestas
    def get_queryset(self):
        return Bet.objects.filter(user=self.request.user).order_by('-created_at')
    
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
        "premier league" : "EPL",
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
    if request.method == "POST":
        quantity = Decimal(request.POST.get('quantity'))
        
        if quantity > 0:
            user_profile = request.user.userprofile
            user_profile.money += quantity
            user_profile.save()
            return redirect('apuestas:home')
            
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

@login_required
def realizar_apuesta(request):
    if request.method == "POST":
        game_id = request.POST.get("game_id")
        selection = request.POST.get("seleccion")
        price = Decimal(request.POST.get("cuota"))
        quantity = Decimal(request.POST.get("cantidad"))
        
        # si algo falta abortamos: 
        if not all([game_id, selection, price, quantity]):
            messages.error(request, "Error: Faltan datos en el boleto.")
            return redirect('apuestas:home')
        
        # si el dinero apostar es incorrecto, abortamos:
        if quantity <= 0:
            messages.error(request, "La cantidad a apostar debe ser mayor que cero.")
            return redirect('apuestas:home')
        
        user_profile = request.user.userprofile
        
        if quantity > user_profile.money:
            messages.error(request, "El usuario no tiene suficiente dinero para realizar esta apuesta.")
            return redirect('apuestas:home')
        
        user_profile.money -= quantity
        user_profile.save()
        
        Bet.objects.create(
            user = request.user,
            game_id = game_id,
            amount = quantity,
            selection = selection,
            price = price
        )
        
        messages.success(request, f"¡Apuesta de {quantity}€ realizada con éxito!")
        return redirect('apuestas:bets_list')
    
    return redirect('apuestas:home')
        
@login_required
def borrar_apuesta(request, bet_id):
    if request.method == "POST":
        # lanza un 404 si la puesta a eliminar no es de ese ususario
        bet = get_object_or_404(Bet, id=bet_id, user=request.user)
        
        # le devolvemos el dinero a l'usuario
        profile = request.user.userprofile
        profile.money += bet.amount
        profile.save()
        
        bet.delete()
        
    return redirect('apuestas:bets_list')


@login_required
def editar_apuesta(request, bet_id):
    if request.method == "POST":
        new_quantity = Decimal(request.POST.get('cantidad_input'))
        bet = get_object_or_404(Bet, id=bet_id, user=request.user)
        
        if new_quantity <= 0:
            messages.error(request, "La cantidad a apostar debe ser mayor que cero.")
            return redirect('apuestas:bets_list')
        
        profile = request.user.userprofile
        if new_quantity > bet.amount and profile.money >= (new_quantity - bet.amount):
            diff = new_quantity - bet.amount
            bet.amount = new_quantity
            profile.money -= diff
            
        elif new_quantity <= bet.amount:
            diff = bet.amount - new_quantity
            profile.money += diff
            bet.amount = new_quantity
            
        bet.save()
        profile.save()
            
    return redirect('apuestas:bets_list')
def buscar_partidos_ajax(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"results": []})

    partidos = Game.objects.filter(
        Q(home_team__icontains=query) | Q(away_team__icontains=query)
    ).order_by("game_date")[:10]

    results = []
    for partido in partidos:
        results.append({
            "game_id": partido.game_id,
            "home_team": partido.home_team,
            "away_team": partido.away_team,
            "league": partido.league,
            "game_date": partido.game_date.strftime("%d/%m/%Y %H:%M"),
        })

    return JsonResponse({"results": results})
        
        
    
        
            
            
            
