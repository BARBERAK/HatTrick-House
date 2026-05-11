from django.urls import path

from . import views

app_name = 'apuestas'

urlpatterns = [
    path('', views.home, name='home'),
    path('apuestas/', views.BetListView.as_view(), name='bets_list'),
    path('update_data/', views.create_update, name="update_data"),
    path('partidos/<str:categoria>/<str:nombre_liga>/', views.partidos_liga, name="partidos_liga"),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('registrar/' , views.register, name="registrar"),
    path('realizar-apuesta/' , views.realizar_apuesta, name="realizar_apuesta")
]