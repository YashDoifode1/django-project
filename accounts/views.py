from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('accounts:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('accounts:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('accounts:login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

from django.contrib.auth.decorators import login_required
from .models import Profile

# accounts/views.py
from django.contrib.auth.decorators import login_required
from products.models import Product
from blog.models import BlogPost

@login_required
def profile_view(request):
    profile = request.user.profile
    user_products = Product.objects.filter()[:4]  # Replace with user-owned if applicable
    user_posts = BlogPost.objects.all()[:4]  # Replace with user-owned if you add authors later

    context = {
        'profile': profile,
        'user_products': user_products,
        'user_posts': user_posts,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Basic info
        profile.bio = request.POST.get('bio', '')
        profile.website = request.POST.get('website', '')
        profile.location = request.POST.get('location', '')
        profile.occupation = request.POST.get('occupation', '')
        profile.company = request.POST.get('company', '')

        # Social links
        profile.linkedin = request.POST.get('linkedin', '')
        profile.github = request.POST.get('github', '')
        profile.twitter = request.POST.get('twitter', '')
        profile.facebook = request.POST.get('facebook', '')
        profile.instagram = request.POST.get('instagram', '')
        profile.youtube = request.POST.get('youtube', '')

        # Preferences (checkboxes)
        profile.email_newsletter = 'email_newsletter' in request.POST
        profile.email_blog = 'email_blog' in request.POST
        profile.email_marketing = 'email_marketing' in request.POST
        profile.profile_public = 'profile_public' in request.POST
        profile.show_email = 'show_email' in request.POST

        # Image upload
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, "✅ Your profile has been updated successfully!")
        return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html', {'profile': profile})