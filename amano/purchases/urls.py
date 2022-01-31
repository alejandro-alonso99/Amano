from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.purchases_list, name='purchases_list'),
]