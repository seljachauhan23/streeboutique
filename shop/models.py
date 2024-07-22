from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.code


class Filter_price(models.Model):
    filter_price = (
        ('200 TO 500', '200 TO 500'),
        ('500 TO 1000', '500 TO 1000'),
        ('1000 TO 5000', '1000 TO 5000'),
        ('5000 TO 10000', '5000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 50000', '20000 TO 50000'),
    )
    
    price = models.CharField(choices=filter_price, max_length=60)
    def __str__(self):
        return self.price

class Product(models.Model):
    condition_choice = (('New', 'New') , ('Sale', 'Sale'), ('50% Off', '50% Off'), ('75% Off', '75% Off'))
    stock = (('In Stock', 'In Stock') , ('Out Of Stock', 'Out Of Stock'))
    status = (('Publish', 'Publish') , ('Draft', 'Draft'))

    u_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/image')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=condition_choice, max_length=100)
    discount = models.IntegerField(null=True, default=0)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=stock,max_length=200)
    # totalStock = models.IntegerField(default=0)
    status = models.CharField(choices=status,max_length=200)
    avl_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories,on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete = models.CASCADE)
    color = models.ForeignKey(Color,on_delete = models.CASCADE)
    filter_price = models.ForeignKey(Filter_price,on_delete = models.CASCADE)

    def __str__(self):
        return self.name

# def save(self,args, **kwargs):
#     if self.id is None and self.avl_date and self.gen_id:
#         self.id = self.avl_date.strftime('75%Y%m%d24') + str(self.gen_id)
#     return Super().save(*args,**kwargs)

def save(self, *args, **kwargs):
        if self.u_id is None and self.avl_date:
            # Assuming self.gen_id is defined elsewhere; otherwise, adjust as needed
            self.u_id = self.avl_date.strftime('%Y%m%d%H%M%S') + str(self.gen_id)
        super(Product, self).save(*args, **kwargs) 


class Images(models.Model): 
    image = models.ImageField(upload_to='product_images/image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    size = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.size
    
class Product_Color(models.Model):
    color = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.color
    
class Contact(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Order(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    post_code = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    additional_info = models.TextField(blank=True, null=True)
    amount = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        # return self.User.user
        return f"Order #{self.id}"
    
    def cancel(self):
        if self.status == 'pending' or self.status == 'processing':
            self.status = 'canceled'
            self.save()
    
    
class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/order_img')
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return f"Order item {self.id}"
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Wishlist of {self.user.username}'
    
class Cart1(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, default=None)
    clr = models.ForeignKey(Product_Color, on_delete=models.CASCADE, default=None)
    image = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=100, default=None)
    price = models.IntegerField(default=None)
    quantity = models.IntegerField(default=None)
    sbt = models.IntegerField(default=None)
    