import imp
from django.shortcuts import render
from .models import Purchases

def purchases_list(request):

    purchases = Purchases.objects.all()

    total_purchases = purchases.count()

    print(purchases[0].calculate_total())

    return render(request, 'purchases/purchases_list.html', {
                                                            'purchases':purchases,
                                                            'total_purchases':total_purchases,
                                                                })
