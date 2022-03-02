from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('create/product/', views.create_product, name='product_create'),
    path('<int:day>/<int:month>/<int:year>/<slug:product>/', views.product_detail, name='product_detail'),
]    