from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_products/', views.view_products, name='view_products'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('view_bill/<int:purchase_id>/', views.view_bill, name='view_bill'),
    path('list_bills/', views.list_bills, name='list_bills'),

]
