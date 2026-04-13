from django.urls import path

from . import views

app_name = 'apuestas'

urlpatterns = [
    path('', views.home, name='home'),
    path('apuestas/', views.GameListView.as_view(), name='games_list'),
    path('update_data/', views.create_update, name="update_data"),
    path('<str:categoria>/<str:nombre_liga>/', views.partidos_liga, name="partidos_liga"),
]