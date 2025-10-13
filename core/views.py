from django.shortcuts import render
from django.core.paginator import Paginator
from products.models import Product, Category as ProductCategory
from blog.models import BlogPost, BlogCategory

from django.shortcuts import render

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)

def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)


def home(request):
    # Fetch categories
    product_categories = ProductCategory.objects.all()
    blog_categories = BlogCategory.objects.all()

    # Fetch products and blogs
    product_list = Product.objects.all()
    blog_list = BlogPost.objects.all()

    # Pagination for products (4 per page, 2x2 grid)
    product_paginator = Paginator(product_list, 4)
    product_page_number = request.GET.get('product_page')
    products = product_paginator.get_page(product_page_number)

    # Pagination for blogs (4 per page, 2x2 grid)
    blog_paginator = Paginator(blog_list, 4)
    blog_page_number = request.GET.get('blog_page')
    blogs = blog_paginator.get_page(blog_page_number)

    context = {
        'product_categories': product_categories,
        'blog_categories': blog_categories,
        'products': products,
        'blogs': blogs,
    }
    return render(request, 'core/home.html', context)



def about(request):
    return render(request, 'core/about.html')

# def contact(request):
#     return render(request, 'core/contact.html')

from django.shortcuts import render
from django.db.models import Q
from products.models import Product
from blog.models import BlogPost

def search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'products')
    results = []

    if query:
        if search_type == 'products':
            results = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        elif search_type == 'blog':
            results = BlogPost.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

    context = {
        'query': query,
        'search_type': search_type,
        'results': results
    }
    return render(request, 'core/search_results.html', context)

from django.shortcuts import render, redirect
from .models import Contact

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            success = "Your message has been submitted successfully!"
            return render(request, 'core/contact.html', {'success': success})
        else:
            error = "All fields are required."
            return render(request, 'core/contact.html', {'error': error})

    return render(request, 'core/contact.html')
