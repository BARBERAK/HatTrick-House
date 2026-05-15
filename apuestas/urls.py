from django.urls import path
from . import views

app_name = 'apuestas'

urlpatterns = [
    path('', views.home, name='home'),
    path('apuestas/', views.BetListView.as_view(), name='bets_list'),
    path('update_data/', views.create_update, name="update_data"),
    path('partidos/<str:categoria>/<str:nombre_liga>/', views.partidos_liga, name="partidos_liga"),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('registrar/', views.register, name="registrar"),
    path('eliminar-apuesta/<int:bet_id>/', views.borrar_apuesta, name='eliminar_apuesta'),
    path('editar-apuesta/<int:bet_id>/', views.editar_apuesta, name='editar_apuesta'),
    path('buscar-partidos-ajax/', views.buscar_partidos_ajax, name='buscar_partidos_ajax'),
    path('realizar-apuesta/', views.realizar_apuesta, name="realizar_apuesta"),
    path('withdraw/', views.withdraw, name="withdraw"),
]