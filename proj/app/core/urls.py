from django.contrib import admin
from django.urls import path, include
from .views import home, transacoes, extrato

urlpatterns = [
    path("", home),
    path("<int:id>/transacoes", transacoes),
    path("<int:id>/extrato", extrato),
]
