from django.urls import path
from . import views

urlpatterns = [
    path('', views.diagram_home, name='diagram-home'),
]
