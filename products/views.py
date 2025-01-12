from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Customer, Purchase
from django.contrib import messages
from django.db.models import Sum
from django.http import Http404

def home(request):
    # Get counts for products, customers, and total sales
    product_count = Product.objects.count()
    customer_count = Customer.objects.count()
    total_sales = Purchase.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    return render(request, 'home.html', {
        'product_count': product_count,
        'customer_count': customer_count,
        'total_sales': total_sales
    })

# Add Product
def add_product(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        prod_name = request.POST.get('prod_name')
        prod_price = request.POST.get('prod_price')
        if date and prod_name and prod_price:
            Product.objects.create(date=date, prod_name=prod_name, prod_price=prod_price)
            messages.success(request, 'Product added successfully!')
            return redirect('add_product')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'add_product.html')

# View Products
def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})

# Remove Product
def remove_product(request):
    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        product = Product.objects.filter(prod_name=prod_name).first()
        if product:
            product.delete()
            messages.success(request, 'Product removed successfully!')
        else:
            messages.error(request, 'Product not found.')
        return redirect('remove_product')
    return render(request, 'remove_product.html')

def generate_bill(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        products_selected = request.POST.getlist('products')

        # Check if all fields are provided
        if customer_name and email and phone and products_selected:
            try:
                # Check if the customer exists, if not, create a new customer
                customer, created = Customer.objects.get_or_create(
                    name=customer_name, email=email, phone=phone)

                # Get selected products
                products = Product.objects.filter(id__in=products_selected)

                # Ensure that the products exist in the database
                if not products:
                    messages.error(request, 'Selected products are invalid.')
                    return redirect('generate_bill')

                # Create a new purchase and assign products
                purchase = Purchase.objects.create(customer=customer)
                purchase.products.set(products)

                # Calculate the total amount and save the purchase
                purchase.calculate_total_amount()

                # Show success message and redirect to view the bill
                messages.success(request, 'Bill generated successfully!')
                return redirect('view_bill', purchase_id=purchase.id)

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('generate_bill')

        else:
            # Error message if any field is missing
            messages.error(request, 'All fields are required.')
            return redirect('generate_bill')
    else:
        # Pass all products to the template for the GET request
        products = Product.objects.all()
        return render(request, 'generate_bill.html', {'products': products})
    
def view_bill(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    return render(request, 'view_bill.html', {'purchase': purchase})

def list_bills(request):
    # Fetch all purchases from the database
    purchases = Purchase.objects.all()

    # Render the template with the list of purchases
    return render(request, 'list_bills.html', {'purchases': purchases})