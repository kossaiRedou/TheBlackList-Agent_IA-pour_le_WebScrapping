from django.contrib import admin
from django.urls import path, include
from .views import index, resultats, historique
urlpatterns = [
    path('', index, name='index'),
    path('resultats/', resultats, name='resultats'),
    path('historique/', historique, name='historique'),
]