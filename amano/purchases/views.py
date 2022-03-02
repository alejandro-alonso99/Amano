from calendar import month
from django.shortcuts import render, get_object_or_404, redirect
from .models import Purchases
from .forms import SearchForm, DateForm, DestroyObjectForm, PurchaseForm
from django.contrib.postgres.search import SearchVector
from stock.models import Product
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def purchases_list(request):

    search_form = SearchForm()
    
    date_form = DateForm()

    query = None

    date_query_start = None
    date_query_end = None

    purchases = Purchases.objects.all()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            purchases = Purchases.objects.annotate(search=SearchVector('proveedor'),).filter(search=query)
        
    if 'date_query_start' and 'date_query_end' in request.GET:
        form = DateForm(request.GET)
        if form.is_valid():
            date_query_start = form.cleaned_data['date_query_start'].strftime("%Y-%m-%d")
            date_query_end = form.cleaned_data['date_query_end'].strftime("%Y-%m-%d")
            purchases = Purchases.objects.filter(fecha__range=[date_query_start, date_query_end])
            
    total_purchases = purchases.count()

    today = datetime.date.today()

    this_month_purchases = Purchases.objects.filter(fecha__month = today.month)
    
    total_month_purchases = this_month_purchases.count()

    month_purchases_totals = []
    for purchase in this_month_purchases:
        purchase_total = purchase.calculate_total()
        month_purchases_totals.append(purchase_total)

    month_total = sum(month_purchases_totals)

    last_purchase = purchases.first()

    for purchase in purchases:
        print(purchase.producto.categoria)

    return render(request, 'purchases/purchases_list.html', {
                                                            'purchases':purchases,
                                                            'search_form':search_form,
                                                            'query':query,
                                                            'date_form':date_form,
                                                            'date_query_start':date_query_start,
                                                            'date_query_end':date_query_end,
                                                            'total_purchases':total_purchases,
                                                            'total_month_purchases':total_month_purchases,
                                                            'month_total':month_total,
                                                            'last_purchase':last_purchase,
                                                                })

@login_required
def purchase_detail(request, year, month, day, purchase):

    purchase = get_object_or_404(Purchases, slug=purchase,
                                                fecha__year = year,
                                                fecha__month = month,
                                                fecha__day = day )

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        purchase.delete()
        
        return redirect('purchases:purchases_list')
        
    else:
        destroy_object_form = DestroyObjectForm()


    return render(request, 'purchases/purchase_detail.html', {
                                                                'purchase':purchase,
                                                                'destroy_object_form':destroy_object_form})                                                

@login_required                                                            
def purchase_create(request):

    products = Product.objects.all()

    if products:

        if request.method == 'POST':
            purchase_form = PurchaseForm(data=request.POST)
            if purchase_form.is_valid():
                purchase_form.save()
            
            return redirect('purchases:purchases_list')

        else:
            purchase_form = PurchaseForm()
    
    else:
        purchase_form = []

    return render(request, 'purchases/purchase_create.html',{ 'purchase_form':purchase_form})
