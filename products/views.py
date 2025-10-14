from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Product, Category

def product_list(request):
    # Base queryset
    products = Product.objects.all()

    # ======== SEARCH FILTER ========
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # ======== CATEGORY FILTER ========
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category__name__in=selected_categories)

    # ======== PRICE RANGE FILTER ========
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # ======== RATING FILTER ========
    rating = request.GET.get('rating')
    if rating:
        products = products.filter(rating__gte=rating)

    # ======== SORTING ========
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'popular':
        products = products.order_by('-review_count')
    else:  # default (newest first)
        products = products.order_by('-id')

    # ======== PAGINATION ========
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ======== CATEGORY COUNTS ========
    categories = Category.objects.annotate(product_count=Count('product'))

    # ======== ACTIVE FILTER TAGS (for UI) ========
    active_filters = []
    if query:
        active_filters.append(f"Search: {query}")
    if selected_categories:
        active_filters += selected_categories
    if min_price or max_price:
        price_range = f"Price: {min_price or '0'} - {max_price or '∞'}"
        active_filters.append(price_range)
    if rating:
        active_filters.append(f"Rating: {rating}★ & Up")

    # ======== CONTEXT ========
    context = {
        'products': page_obj,
        'total_products': Product.objects.count(),
        'categories': categories,
        'selected_categories': selected_categories,
        'active_filters': active_filters,
        'request': request,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Related products (same category, exclude current product)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]

    # Convert comma-separated fields to lists if using CharField/TextField
    key_features_list = product.key_features.split(',') if product.key_features else []
    specifications_list = []
    if product.specifications:
        # assuming specifications stored like "Key1:Value1,Key2:Value2"
        for spec in product.specifications.split(','):
            if ':' in spec:
                name, value = spec.split(':', 1)
                specifications_list.append({'name': name.strip(), 'value': value.strip()})

    context = {
        'product': product,
        'related_products': related_products,
        'key_features_list': key_features_list,
        'specifications_list': specifications_list,
    }

    return render(request, 'products/product_detail.html', context)