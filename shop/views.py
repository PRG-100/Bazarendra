from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, Order, OrderItem

PRIMARY = "#55a656"

def _get_cart(request):
    cart = request.session.get('cart', {})
    return cart

def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'PRIMARY': PRIMARY})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product, 'PRIMARY': PRIMARY})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart(request)
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    _save_cart(request, cart)
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('shop:view_cart')

def remove_from_cart(request, pk):
    cart = _get_cart(request)
    cart.pop(str(pk), None)
    _save_cart(request, cart)
    messages.info(request, "Item removed from cart.")
    return redirect('shop:view_cart')

def view_cart(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))
        subtotal = product.price * qty
        items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'shop/cart.html', {'items': items, 'total': total, 'PRIMARY': PRIMARY})

def checkout(request):
    cart = _get_cart(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('shop:product_list')
        if not all([name, email, address]):
            messages.error(request, "Please fill in all fields.")
            return render(request, 'shop/checkout.html', {'PRIMARY': PRIMARY})
        order = Order.objects.create(customer_name=name, customer_email=email, address=address)
        for pid, qty in cart.items():
            product = get_object_or_404(Product, pk=int(pid))
            OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
        _save_cart(request, {})
        return redirect(reverse('shop:order_success', args=[order.id]))
    return render(request, 'shop/checkout.html', {'PRIMARY': PRIMARY})

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shop/order_success.html', {'order': order, 'PRIMARY': PRIMARY})
