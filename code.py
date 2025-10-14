# populate_blog.py
import os
import django
import random
from datetime import datetime, timedelta

# -----------------------------
# Setup Django environment
# -----------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affiliate_site.settings')  # Update to your settings module
django.setup()

from blog.models import BlogPost, BlogCategory
from django.contrib.auth.models import User  # Assuming you want to assign authors

# -----------------------------
# Utility Data
# -----------------------------
categories_data = ['IT', 'Cybersecurity', 'Data Science', 'IoT']
sample_titles = [
    '10 Tips for', 'The Future of', 'How to Master', 'Understanding', 'Beginner’s Guide to',
    'Top 5 Tools for', 'Common Mistakes in', 'Best Practices for', 'Exploring', 'The Ultimate Guide to'
]
sample_contents = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ac neque nec libero malesuada aliquam.',
    'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;',
    'Integer ac turpis at nulla fermentum tincidunt. Sed vitae dui vitae libero tincidunt imperdiet.',
    'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.',
    'Suspendisse potenti. Phasellus a felis sit amet turpis vehicula laoreet.',
]

# -----------------------------
# Create categories if not exist
# -----------------------------
categories = {}
for cat_name in categories_data:
    cat_obj, created = BlogCategory.objects.get_or_create(name=cat_name)
    categories[cat_name] = cat_obj

# -----------------------------
# Create dummy authors if none exist
# -----------------------------
authors = list(User.objects.all())
if not authors:
    # Create a default superuser
    user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
    authors.append(user)

# -----------------------------
# Function to generate dummy blog posts
# -----------------------------
def create_dummy_blogs(num_per_category=5):
    for cat_name, cat_obj in categories.items():
        for i in range(1, num_per_category + 1):
            title = f"{random.choice(sample_titles)} {cat_name} Topic {i}"
            content = random.choice(sample_contents) * random.randint(2, 5)
            author = random.choice(authors)
            created_at = datetime.now() - timedelta(days=random.randint(0, 365))  # Random date within last year

            # Create blog post
            post = BlogPost.objects.create(
                title=title,
                content=content,
                category=cat_obj,
                created_at=created_at,
            )

    print(f"Dummy blog posts created successfully! ({num_per_category} per category)")

# -----------------------------
# Execute
# -----------------------------
if __name__ == '__main__':
    create_dummy_blogs(num_per_category=5)
