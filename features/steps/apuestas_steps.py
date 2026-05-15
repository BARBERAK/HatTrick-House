from behave import given, when, then
from django.contrib.auth.models import User
from apuestas.models import UserProfile, Game, Bet
from django.utils import timezone
from decimal import Decimal

# --- GIVEN (Preparación de la Base de Datos) ---

@given('Existe un usuario "{username}" con contraseña "{password}" y saldo "{saldo}"')
def step_create_user(context, username, password, saldo):
    user = User.objects.create_user(username=username, password=password)
    perfil = user.userprofile
    perfil.money = Decimal(saldo)
    perfil.save()

@given('El usuario inicia sesión con "{username}" y "{password}"')
def step_login(context, username, password):
    context.browser.visit(context.base_url + '/accounts/login/') 
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    context.browser.find_by_css('button[type="submit"]').first.click()

@given('Existe un partido "{home}" vs "{away}" con id "{game_id}"')
def step_create_game(context, home, away, game_id):
    Game.objects.create(
        game_id=game_id, 
        home_team=home, 
        away_team=away, 
        home_price=2.50, 
        away_price=3.00, 
        game_date=timezone.now()
    )

@given('El usuario tiene una apuesta de "{amount}" euros en el partido "{game_id}"')
def step_create_bet(context, amount, game_id):
    user = User.objects.get(username="testuser")
    game = Game.objects.get(game_id=game_id)
    Bet.objects.create(user=user, game=game, amount=Decimal(amount), selection='1', price=2.50)
    
    # Le restamos el dinero del saldo para simular que ya la hizo
    perfil = user.userprofile
    perfil.money -= Decimal(amount)
    perfil.save()


# --- WHEN (Acciones del usuario en el navegador) ---

@when('El usuario visita la página del partido "{game_id}"')
def step_visit_game(context, game_id):
    # Vamos a la ruta donde tienes el listado de partidos
    context.browser.visit(context.base_url + '/partidos/soccer/LaLiga/') 

@when('Selecciona la opción "{selection}" con cuota "{cuota}"')
def step_select_odd(context, selection, cuota):
    # HACK: Como el robot "django" no ejecuta JavaScript, rellenamos los 
    # inputs hidden directamente basándonos en tu bet_slip.html
    context.browser.fill('game_id', 'game1')
    context.browser.fill('seleccion', selection)
    context.browser.fill('cuota', cuota)

@when('Introduce la cantidad "{cantidad}"')
def step_fill_amount(context, cantidad):
    context.browser.fill('cantidad', cantidad)

@when('Hace clic en "{texto_boton}"')
@when('El usuario hace clic en "{texto_boton}"')
def step_click_button(context, texto_boton):
    # Intenta buscar el botón primero por "value" (<input type="submit">) y si no, por texto (<button>)
    if context.browser.is_element_present_by_value(texto_boton):
        context.browser.find_by_value(texto_boton).first.click()
    else:
        context.browser.find_by_text(texto_boton).first.click()

@when('El usuario visita la página de sus apuestas')
def step_visit_my_bets(context):
    context.browser.visit(context.base_url + '/apuestas/')

@when('El usuario edita la apuesta al nuevo valor de "{nueva_cantidad}" euros')
def step_edit_bet(context, nueva_cantidad):
    # Viajamos directamente a la URL de edición para evitar que el navegador se pierda buscando enlaces
    apuesta = Bet.objects.first()
    context.browser.visit(context.base_url + f'/editar-apuesta/{apuesta.id}/')
    
    context.browser.fill('cantidad', nueva_cantidad)
    context.browser.find_by_text('Guardar Cambios').first.click()


# --- THEN (Comprobaciones finales) ---

@then('Se muestra un mensaje de éxito')
def step_check_success_message(context):
    # Buscamos palabras clave en todo el HTML, es infalible sin importar la clase CSS
    html_de_la_pagina = context.browser.html.lower()
    assert "éxito" in html_de_la_pagina or "correctamente" in html_de_la_pagina, "No se encontró el texto de éxito."

@then('Se muestra un mensaje de error diciendo "{mensaje}"')
def step_check_error_message(context, mensaje):
    assert context.browser.is_text_present(mensaje, wait_time=2)

@then('La apuesta aparece en su lista de "Mis Apuestas"')
def step_check_bet_in_list(context):
    context.browser.visit(context.base_url + '/apuestas/')
    assert context.browser.is_text_present('Real Madrid vs Barcelona', wait_time=2)

@then('La apuesta desaparece de "Mis Apuestas"')
def step_check_bet_not_in_list(context):
    context.browser.visit(context.base_url + '/apuestas/')
    assert context.browser.is_text_not_present('Real Madrid vs Barcelona', wait_time=2)

@then('La apuesta original de "{cantidad}" euros se mantiene')
def step_check_original_bet(context, cantidad):
    context.browser.visit(context.base_url + '/apuestas/')
    assert context.browser.is_text_present(f'{cantidad}', wait_time=2)

@then('El saldo del usuario es "{saldo_esperado}"')
@then('El saldo del usuario vuelve a ser "{saldo_esperado}"')
def step_check_balance(context, saldo_esperado):
    # Recarga el perfil desde la BD para ver si las matemáticas fueron correctas
    user = User.objects.get(username="testuser")
    assert user.userprofile.money == Decimal(saldo_esperado)