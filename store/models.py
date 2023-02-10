from django.db import models
from django.urls import reverse
from category.models import Category
from django.utils.safestring import mark_safe
from accounts.models import Account
from django.db.models import Avg, Count


# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500,blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category,  on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ProductReview.objects.filter(product=self).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ProductReview.objects.filter(product=self).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class Size(models.Model):
    name  = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value
    
class Color(models.Model):
    name = models.CharField(max_length=10)
    value = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
    def color(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.value))


class ProductVariation(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='store/products' , max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'