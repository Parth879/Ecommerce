from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from store.models import Product, ProductVariation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    variantid = request.POST.get('variantid')

    price = ProductVariation.objects.filter(id=variantid)
    for price in price:
        product_price = price.price


    if current_user.is_authenticated:

        try:    # get the cart id by cart function to store product into cart
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cart id present in session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        
        is_cart_item_exists = CartItem.objects.filter(product=product,  variant=variantid,user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product,  variant=variantid,user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
                cart = cart,
                variant = ProductVariation(id=variantid),
                price = product_price
            )
            cart_item.save()
        return redirect('cart')

    # WITHOUT LOGIN
    else:

        try:    # get the cart id by cart function to store product into cart
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cart id present in session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, variant=variantid,cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, variant=variantid,cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                variant = ProductVariation(id=variantid),
                price = product_price
            )
            cart_item.save()
        return redirect('cart')




def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total

    }
    return render(request, 'store/cart.html', context)

def plus_cart(request, cart_id):
    cart_item = get_object_or_404(CartItem, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')
    

def remove_cart(request,cart_id):
    cart_item = get_object_or_404(CartItem, id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, cart_id):
    cart_item = get_object_or_404(CartItem, id=cart_id)
    cart_item.delete()
    return redirect('cart')



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'store/checkout.html' ,context)