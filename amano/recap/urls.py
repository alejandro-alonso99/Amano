from unicodedata import name
from django.urls import path
from . import views

app_name = 'recap'

urlpatterns = [
    path('', views.recap_list, name='recap_list'),
    path('create/',views.recap_create, name='recap_create')
]
