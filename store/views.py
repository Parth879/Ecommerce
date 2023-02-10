from django.shortcuts import get_object_or_404, redirect, render
from category.models import Category
from store.forms import ReviewForm
from .models import Product, ProductGallery, ProductReview, ProductVariation
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
# Create your views here.


def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 50)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products':paged_products,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    related_products = Product.objects.exclude(slug=product_slug).filter(is_available=True,category__slug=category_slug)
    all_rev = Paginator(ProductReview.objects.filter(product=single_product), 3)
    page = request.GET.get('page')
    try:
        rprod = all_rev.page(page)
    except PageNotAnInteger:
        rprod = all_rev.page(1)
    except EmptyPage:
        rprod = all_rev.page(all_rev.num_pages)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product':single_product,
        'related_products': related_products,
        'rprod':rprod,
        'all_rev':all_rev,
        'product_gallery':product_gallery
    }
    query = request.GET.get('q')
    id = single_product.id
    if request.method == 'POST':
        variant_id = request.POST.get('variantid')
        variant = ProductVariation.objects.get(id=variant_id)
        colors = ProductVariation.objects.filter(product=id,size_id=variant.size_id)
        sizes = ProductVariation.objects.raw('SELECT * FROM store_productvariation WHERE product_id=%s GROUP BY size_id',[id])
        query += variant.name+' Size:' +str(variant.size) + 'Color: ' + str(variant.color)
    else:
        variants = ProductVariation.objects.filter(product=id) 
        colors = ProductVariation.objects.filter(product=id, size_id=variants[0].size_id)
        sizes = ProductVariation.objects.raw('SELECT * FROM store_productvariation WHERE product_id=%s GROUP BY size_id',[id])
        variant = ProductVariation.objects.get(id=variants[0].id)
    
    context.update({ 'sizes': sizes, 'colors': colors, 'variant': variant, 'query': query})

    return render(request, 'store/product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = ProductVariation.objects.filter(product=productid, size=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('store/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products':products,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)


def review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ProductReview.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank You! Your review has been updated.")
            return redirect(url)
        
        except ProductReview.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ProductReview()
                data.subject = form.cleaned_data['subject']
                data.rating  = form.cleaned_data['rating']
                data.review  = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank You! Your review has been Sumited")
                return redirect(url)