from django.urls import path

from . import views

app_name = 'apuestas'

urlpatterns = [
    path('', views.home, name='home'),
]