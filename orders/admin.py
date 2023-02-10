from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.

class AdminPayment(admin.ModelAdmin):
    list_display = ('user','payment_id','payment_method','amount_paid','status','created_at')

class AdminOrder(admin.ModelAdmin):
    list_display = ('user','payment','order_number','first_name','last_name','phone','email','address_line_1','country','state','city','order_note','order_total','tax','status','ip','is_ordered','created_at','updated_at')

class AdminOrderProduct(admin.ModelAdmin):
    list_display = ('order','payment','user','product','variation','color','size','quantity','product_price','ordered','created_at','updated_at')

admin.site.register(Payment,AdminPayment)
admin.site.register(Order,AdminOrder)
admin.site.register(OrderProduct,AdminOrderProduct)