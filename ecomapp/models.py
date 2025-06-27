from django.db import models

from django.contrib.auth.models import User                                    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)                 
    adminfullname = models.CharField(max_length=50)
    adminimage = models.ImageField(upload_to="admins")
    adminmobile = models.CharField(max_length=20)
    adminaddress = models.CharField(max_length=200, null=True, blank=True)           
    is_employee =models.BooleanField(default=True)


    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)                 
    customerfullname = models.CharField(max_length=200)
    customeraddress = models.CharField(max_length=200, null=True, blank=True)                                 
    customermobile = models.CharField(max_length=20)

    def __str__(self):
        return self.customerfullname                                                   



class Category(models.Model):
    categorytitle = models.CharField(max_length=200)
    categoryslug = models.SlugField(unique=True)

    def __str__(self):
        return self.categorytitle                                                       

class Product(models.Model):
    categoryname = models.ForeignKey(Category, on_delete=models.CASCADE)            
    producttitle = models.CharField(max_length=200)
    productslug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products")
    productprice = models.PositiveIntegerField()
    productdescription = models.TextField()      

    def __str__(self):
        return self.producttitle                                                      


class ProductImage(models.Model):                                               
    product = models.ForeignKey(Product, on_delete=models.CASCADE)              
    image = models.ImageField(upload_to="products/images/")                     

    def __str__(self):
        return self.product.producttitle



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)    
    total = models.PositiveIntegerField(default=0)                                              
    created_at = models.DateTimeField(auto_now_add=True)                                        
    def __str__(self):
        return "Cart: " + str(self.id)                                                          


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)

ostatus = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Online Payment", "Online Payment"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    productorderedby = models.CharField(max_length=200)
    productshippingaddress = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    ostatus = models.CharField(max_length=50, choices=ostatus)            
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id)











