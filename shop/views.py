from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .parser import get_html, get_page_data
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            products = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'shop/product/list_ajax.html', locals())
    return render(request, 'shop/product/list.html', locals())


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', locals())


def parser(url, category):
    products = get_page_data(get_html(url))
    for i in products:
        product = Product(name=i[0], price=i[1], image_out_source=i[2], description=i[3], category=category)
        product.save()
    return f'NO OK'


# url = 'https://www.kivano.kg/mobilnye-telefony'
# smartphones = Category.objects.get(name='smartphones')
# parser(url, smartphones)