# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import BlogPost, BlogCategory

def blog_list(request):
    posts = BlogPost.objects.all()
    selected_categories = request.GET.getlist('category')
    search_query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_option = request.GET.get('sort', 'newest')

    # Filter by search
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Filter by categories
    if selected_categories:
        posts = posts.filter(category__name__in=selected_categories)

    # Filter by date range
    if start_date:
        posts = posts.filter(created_at__date__gte=start_date)
    if end_date:
        posts = posts.filter(created_at__date__lte=end_date)

    # Sorting
    if sort_option == 'newest':
        posts = posts.order_by('-created_at')
    elif sort_option == 'oldest':
        posts = posts.order_by('created_at')
    elif sort_option == 'title_asc':
        posts = posts.order_by('title')
    elif sort_option == 'title_desc':
        posts = posts.order_by('-title')
    # 'popular' sorting can be implemented if you have a 'views' field
    elif sort_option == 'popular':
        posts = posts.order_by('-views')

    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Categories with post counts
    categories = BlogCategory.objects.annotate(post_count=Count('posts'))

    # Popular tags (dummy example, assuming you have a Tag model)
    popular_tags = []  # Replace with actual tag queryset if you have tags

    # Active filters for template
    active_filters = []
    if search_query:
        active_filters.append(f'Search: "{search_query}"')
    active_filters.extend(selected_categories)
    if start_date:
        active_filters.append(f'Start: {start_date}')
    if end_date:
        active_filters.append(f'End: {end_date}')
    if sort_option:
        active_filters.append(f'Sort: {sort_option.capitalize()}')

    return render(request, 'blog/blog_list.html', {
        'posts': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'active_filters': active_filters,
        'popular_tags': popular_tags,
        'total_posts': posts.count(),
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.order_by('-created_at')

    # Handle new comment
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect(comment.post.get_absolute_url())
        else:
            return redirect('login')
    else:
        form = CommentForm()

    recent_posts = BlogPost.objects.order_by('-created_at')[:5]

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'recent_posts': recent_posts,
    })

