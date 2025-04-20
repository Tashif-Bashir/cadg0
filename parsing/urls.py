from django.urls import path
from . import views 
from .views import upload_file, view_parsed_data


urlpatterns = [
    #path('', views.parsing_home, name='parsing-home'),
    path('upload/', views.upload_file, name='upload-file'),
    path("parsed-data/", view_parsed_data, name="view-parsed-data"),
]
