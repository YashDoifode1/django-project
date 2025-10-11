import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affiliate_site.settings')  # replace 'core.settings' with your settings module
django.setup()

from products.models import Product, Category  # Correct model name

# Fetch categories
it = Category.objects.get(name='IT')
cyber = Category.objects.get(name='Cybersecurity')
ds = Category.objects.get(name='Data Science')
iot = Category.objects.get(name='IoT')

# Create products for IT
Product.objects.create(
    title='IT Product 1',
    description='Description for IT Product 1',
    category=it,
    affiliate_link='https://example.com/it-product-1',
    image='products/default.jpeg'
)
Product.objects.create(
    title='IT Product 2',
    description='Description for IT Product 2',
    category=it,
    affiliate_link='https://example.com/it-product-2',
    image='products/default.jpeg'
)

# Create products for Cybersecurity
Product.objects.create(
    title='Cyber Product 1',
    description='Description for Cyber Product 1',
    category=cyber,
    affiliate_link='https://example.com/cyber-product-1',
    image='products/default.jpeg'
)
Product.objects.create(
    title='Cyber Product 2',
    description='Description for Cyber Product 2',
    category=cyber,
    affiliate_link='https://example.com/cyber-product-2',
    image='products/default.jpeg'
)

# Create products for Data Science
Product.objects.create(
    title='DS Product 1',
    description='Description for DS Product 1',
    category=ds,
    affiliate_link='https://example.com/ds-product-1',
    image='products/default.jpeg'
)
Product.objects.create(
    title='DS Product 2',
    description='Description for DS Product 2',
    category=ds,
    affiliate_link='https://example.com/ds-product-2',
    image='products/default.jpeg'
)

# Create products for IoT
Product.objects.create(
    title='IoT Product 1',
    description='Description for IoT Product 1',
    category=iot,
    affiliate_link='https://example.com/iot-product-1',
    image='products/default.jpeg'
)
Product.objects.create(
    title='IoT Product 2',
    description='Description for IoT Product 2',
    category=iot,
    affiliate_link='https://example.com/iot-product-2',
    image='products/default.jpeg'
)

print("Products created successfully!")
