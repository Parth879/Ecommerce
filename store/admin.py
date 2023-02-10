from django.contrib import admin
from .models import Product, ProductReview, ProductVariation, Size, Color, ProductGallery
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','images','stock','category','created_date','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline]

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('name','product','size','color','price','stock','is_active')
    list_editable = ('is_active','stock')
    list_filter = ('product','size','color','price')


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductReview)
admin.site.register(ProductGallery)
