from re import search
from django.shortcuts import render
from .models import Purchases
from .forms import SearchForm, DateForm
from django.contrib.postgres.search import SearchVector

def purchases_list(request):

    search_form = SearchForm()
    
    date_form = DateForm()

    query = None

    date_query = None

    purchases = Purchases.objects.all()

    total_purchases = purchases.count()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            purchases = Purchases.objects.annotate(search=SearchVector('proveedor'),).filter(search=query)
        
    if 'date_query' in request.GET:
        form = DateForm(request.GET)
        if form.is_valid():
            date_query = form.cleaned_data['date_query']
            purchases = Purchases.objects.filter(fecha__year=date_query.year, fecha__month=date_query.month, fecha__day=date_query.day)
            print(date_query)
    

    return render(request, 'purchases/purchases_list.html', {
                                                            'purchases':purchases,
                                                            'total_purchases':total_purchases,
                                                            'search_form':search_form,
                                                            'query':query,
                                                            'date_form':date_form,
                                                            'date_query':date_query,
                                                                })
