import datetime
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ChangePriceForm, ChangePriceWithAmountForm, ManualmoveForm, ProductForm
from .models import Product, ManualMove
from purchases.forms import DateForm, SearchForm
from django.contrib.postgres.search import SearchVector
from purchases.models import Purchases
from sales.models import Sale
from django.contrib.auth.decorators import login_required
from purchases.forms import DestroyObjectForm

@login_required
def stock_list(request):

    search_form = SearchForm()
    
    date_form = DateForm()

    query = None

    date_query_start = None
    date_query_end = None

    products = Product.objects.all()

    total_products = products.count()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.annotate(search=SearchVector('nombre'),).filter(search=query)
        
    if 'date_query_start' and 'date_query_end' in request.GET:
        form = DateForm(request.GET)
        if form.is_valid():
            date_query_start = form.cleaned_data['date_query_start'].strftime("%Y-%m-%d")
            date_query_end = form.cleaned_data['date_query_end'].strftime("%Y-%m-%d")
            products = Product.objects.filter(fecha_agregado__range=[date_query_start, date_query_end])
    
    product_dict = {}
    for product in products:
        product_purchases = Purchases.objects.filter(producto=product)
        product_sales = Sale.objects.filter(product=product)
        product_manualmoves = ManualMove.objects.filter(product=product)

        product_manualmove_substract = product_manualmoves.filter(tipo='quitar')

        product_manualmove_add = product_manualmoves.filter(tipo='agregar')

        total_substract = sum(list(map(int, product_manualmove_substract.values_list('cantidad', flat=True))))

        total_add = sum(list(map(int, product_manualmove_add.values_list('cantidad', flat=True))))

        total_product_purchases = sum(list(map(int, product_purchases.values_list('cantidad', flat=True))))

        total_product_sales = sum(list(map(int, product_sales.values_list('cantidad', flat=True))))

        total_product_stock = total_product_purchases - total_product_sales + total_add - total_substract

        product_dict[product] = total_product_stock
    
    stock_total = 0
    for product,stock in product_dict.items():
        stock_total += stock
    
    total_products = Product.objects.all().count()

    change_price_form  = ChangePriceForm()

    if 'amount' in request.GET:
        change_price_form = ChangePriceForm(request.GET)
        if change_price_form.is_valid():
            amount = change_price_form.cleaned_data['amount']
            for product in products:
                product.precio_venta += (product.precio_venta * (amount/100))
                product.save()

            return redirect('stock:stock_list')

    this_month = datetime.datetime.now().month
    this_month_products = products.filter(fecha_agregado__month= this_month).count()

    if products:
        last_product = list(products)[-1]
    else: 
        last_product = ''
    return render(request, 'stock/stock_list.html',{'product_dict': product_dict,
                                                    'total_products':total_products,
                                                    'search_form':search_form,
                                                    'query':query,
                                                    'date_form':date_form,
                                                    'date_query_start':date_query_start,
                                                    'date_query_end':date_query_end,
                                                    'total_products':total_products,
                                                    'stock_total':stock_total,
                                                    'change_price_form':change_price_form,
                                                    'this_month_products':this_month_products,
                                                    'last_product':last_product})                                                
@login_required
def create_product(request):

    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid:
            product_form.save()

        return redirect('stock:stock_list')
    
    else:
        product_form = ProductForm()

    return render(request, 'stock/product_create.html', {'product_form':product_form})


@login_required
def product_detail(request, year, month, day, product):

    product = get_object_or_404(Product, slug=product,
                                                    fecha_agregado__year=year,
                                                    fecha_agregado__month=month,
                                                    fecha_agregado__day=day )

    change_price_form  = ChangePriceForm()
    change_individual_price_form = ChangePriceWithAmountForm()

    if request.method == 'POST':
        destroy_object_form = DestroyObjectForm(request.POST)
        product.delete()
        
        return redirect('stock:stock_list')
        
    else:
        destroy_object_form = DestroyObjectForm()

    if 'amount' in request.GET:
        change_price_form = ChangePriceForm(request.GET)
        if change_price_form.is_valid():

            amount = change_price_form.cleaned_data['amount']

            product.precio_venta += (product.precio_venta * (amount/100))
            product.save()

            return redirect(product.get_absolute_url())
    
    if 'ind_amount' in request.GET:
        change_individual_price_form = ChangePriceWithAmountForm(request.GET)
        if change_individual_price_form.is_valid():

            ind_amount = change_individual_price_form.cleaned_data['ind_amount']

            product.precio_venta = ind_amount
            product.save()

            return redirect(product.get_absolute_url())
    


    return render(request, 'stock/product_detail.html',{'product':product,
                                                        'detroy_object_form':destroy_object_form,
                                                        'change_price_form':change_price_form,
                                                        'change_individual_price_form':change_individual_price_form,})                                                

@login_required
def add_manualmove(request):

    products = Product.objects.all()

    manualmove_form = ManualmoveForm(request.POST or None)
    
    if manualmove_form.is_valid():
        manualmove_form.save()

        return redirect('stock:stock_list')

    return render(request, 'stock/manualmove_create.html',{'manualmove_form':manualmove_form, 'products':products})                                                        