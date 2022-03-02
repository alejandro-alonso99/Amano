from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('purchases/', include('purchases.urls', namespace='purchases')),
    path('', include('stock.urls', namespace='stock')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('recap/', include('recap.urls', namespace='recap')),
]
