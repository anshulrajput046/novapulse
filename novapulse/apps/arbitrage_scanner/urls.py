

from django.urls import path
from . import views

urlpatterns = [
    path('scanner/', views.index, name='index'),
]
