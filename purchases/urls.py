from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.purchases_list, name='purchases_list'),
    path('<int:day>/<int:month>/<int:year>/<slug:purchase>/', views.purchase_detail, name='purchase_detail'),
    path('create/', views.purchase_create, name='purchase_create'),
]