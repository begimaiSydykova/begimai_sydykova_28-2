from django.shortcuts import render, redirect
from posts.models import Product, Reviews

from posts.forms import ProductCreateForm, ReviewCreateForm
from posts.constants import PAGINATION_LIMIT
# Create your views here.

def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')
    

def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        ''' PAGINATION_LIMIT, page, products '''

        products = products[PAGINATION_LIMIT * (page-1) : PAGINATION_LIMIT * page]


        if search:
            products = products.filter(title__contains=search) | products.filter(description__contains=search)
        
        context = {
            'products': products,
            'user': request.user,
            'pages': range(1, max_page+1)
        }
        return render(request, 'products/products.html', context=context)

def product_detail_view(request, id_):
    if request.method == 'GET':
        product = Product.objects.get(id=id_)

        context = {
            'product': product,
            'reviews': product.reviews_set.all()
        }
        return render(request, 'products/detail.html', context=context)
    
def product_create_view(request):
    if request.method == 'GET':

        context = {
            'form': ProductCreateForm
        }

        return render(request, 'products/create.html')
    
    if request.method == 'POST':
        data, files = request.POST, request.FILES
        form = ProductCreateForm(data, files)

        if form.is_valid():
            Product.objects.create(
                image = form.cleaned_data.get('image'),
                title = form.cleaned_data.get('title'),
                description = form.cleaned_data.get('description'),
                price = form.cleaned_data.get('price')
            )

            return redirect('/products/')
        
        return render(request, 'products/create.html', context={
            'form': form
        })
    

def review_create_view(request):
    if request.method == 'GET':

        context = {
            'form': ReviewCreateForm
        }

        return render(request, 'products/createreviews.html')
    
    if request.method == 'POST':
        data = request.POST
        form = ReviewCreateForm(data)

        if form.is_valid():
            Reviews.objects.create(
                text = form.cleaned_data.get('text'),
                product = form.cleaned_data.get('product'),
            )

            return redirect('/products/')
        
        return render(request, 'products/createreviews.html', context={
            'form': form
        })