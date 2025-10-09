from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

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
