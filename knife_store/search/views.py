from django.shortcuts import render
from products.models import Product
from .forms import ProductSearchForm


def product_search(request):
    products = Product.objects.all()
    form = ProductSearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['brand'] and form.cleaned_data['brand'] != '':
            products = products.filter(brand__icontains=form.cleaned_data['brand'])
        if form.cleaned_data['clas']:
            products = products.filter(clas__icontains=form.cleaned_data['clas'])
        if form.cleaned_data['year']:
            products = products.filter(year=form.cleaned_data['year'])
        if form.cleaned_data['price_min']:
            products = products.filter(price__gte=form.cleaned_data['price_min'])
        if form.cleaned_data['price_max']:
            products = products.filter(price__lte=form.cleaned_data['price_max'])
    return render(request, 'search/product_search.html', {'form': form, 'products': products})
