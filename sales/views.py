from django.shortcuts import get_object_or_404, render, redirect
from .models import Sale
from .forms import SaleForm
from purchases.forms import SearchForm, DateForm
from django.contrib.postgres.search import SearchVector
from stock.models import Product
import datetime
from purchases.forms import DestroyObjectForm
from django.contrib.auth.decorators import login_required

@login_required
def sales_list(request):

    search_form = SearchForm()
    
    date_form = DateForm()

    query = None

    date_query_start = None
    date_query_end = None

    sales = Sale.objects.all()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            sales = Sale.objects.annotate(search=SearchVector('cliente'),).filter(search=query)
        
    if 'date_query_start' and 'date_query_end' in request.GET:
        form = DateForm(request.GET)
        if form.is_valid():
            date_query_start = form.cleaned_data['date_query_start'].strftime("%Y-%m-%d")
            date_query_end = form.cleaned_data['date_query_end'].strftime("%Y-%m-%d")
            sales = Sale.objects.filter(fecha__range=[date_query_start, date_query_end])

    total_sales = sales.count()

    today = datetime.date.today()

    this_month_sales = Sale.objects.filter(fecha__month = today.month)
    
    total_month_sales = this_month_sales.count()

    month_sales_totals = []
    for sale in this_month_sales:
        sale_total = sale.calculate_total()
        month_sales_totals.append(sale_total)

    month_total= sum(month_sales_totals)

    last_sale = sales.first()

    return render(request, 'sales/sales_list.html', {'sales':sales,
                                                    'search_form':search_form,
                                                    'query':query,
                                                    'date_form':date_form,
                                                    'date_query_start':date_query_start,
                                                    'date_query_end':date_query_end,
                                                    'total_sales':total_sales,
                                                    'total_month_sales':total_month_sales,
                                                    'month_total':month_total,
                                                    'last_sale':last_sale})
@login_required
def sale_create(request):

    products = Product.objects.all()

    if products:

        if request.method == 'POST':
            sale_form = SaleForm(data=request.POST)
            if sale_form.is_valid():
                sale_form.save()
            
            return redirect('sales:sale_list')

        else:
            sale_form = SaleForm()
    
    else:
        sale_form = []

    return render(request, 'sales/sale_create.html', {'sale_form':sale_form})

@login_required
def sale_detail(request, year, month, day, sale):

    sale = get_object_or_404(Sale, slug = sale,
                                fecha__year = year,
                                fecha__month = month,
                                fecha__day = day
                                )

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        sale.delete()
        
        return redirect('sales:sale_list')
        
    else:
        destroy_object_form = DestroyObjectForm()                                

    return render(request, 'sales/sale_detail.html',{'sale':sale,
                                                    'destroy_object_form':destroy_object_form})