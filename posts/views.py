from django.shortcuts import render, redirect
from posts.models import Product, Reviews
from django.views.generic import ListView, DetailView, CreateView
from posts.forms import ProductCreateForm, ReviewCreateForm
from posts.constants import PAGINATION_LIMIT


# Create your views here.

class MainPageCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductsCBV(ListView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'products/products.html'

    def get(self, request, *args, **kwargs):
        products = self.queryset
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
        return render(request, self.template_name, context=context)

class ProductDetailCBV(DetailView, CreateView):
    model = Product
    template_name = 'products/detail.html'
    form_class = ReviewCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'product': self.get_object(),
            'reviews': Reviews.objects.filter(product=self.get_object()),
            'form': kwargs.get('form', self.form_class)
        }

    def post(self, request, **kwargs):

        data = request.POST
        form = ReviewCreateForm(data=data)

        if form.is_valid():
            Reviews.objects.create(
                text=form.cleaned_data.get('text'),
                product_id=self.get_object().id
            )
            return redirect(f'/products/{self.get_object().id}/')

        return render(request, self.template_name, context=self.get_context_data(
            form=form
        ))

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
