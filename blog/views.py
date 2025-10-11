from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory

def blog_list(request):
    # Get category filter from query params
    category_name = request.GET.get('category')

    if category_name:
        posts = BlogPost.objects.filter(category__name=category_name)
    else:
        posts = BlogPost.objects.all()

    categories = BlogCategory.objects.all()

    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'active_category': category_name,
    })


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Fetch other categories and recent posts for sidebar
    categories = BlogCategory.objects.all()
    recent_posts = BlogPost.objects.exclude(pk=pk).order_by('-created_at')[:5]

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'categories': categories,
        'recent_posts': recent_posts,
    })
