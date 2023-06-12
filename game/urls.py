from django.contrib import admin
from django.urls import path, include
from game import views

app_name = 'game'

urlpatterns = [
    path('', views.game, name="game"),
    path('make_move/<int:position>/', views.make_move, name='make_move'),
    path('waitingmove/', views.waitingmove, name='waitingmove'),
]
