from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    date = models.DateField()
    prod_name = models.CharField(max_length=50)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.prod_name

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Default value to prevent errors
    purchase_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Purchase by {self.customer.name} on {self.purchase_date}"

    def calculate_total_amount(self):
        self.total_amount = sum(product.prod_price for product in self.products.all())  # Assuming 'prod_price' is the correct field
        self.save()  # Ensure that the total_amount is saved