from products.models import Keyboard
from .models import Cart, CartItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt

#View Cart
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(user=None)
        
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    
    cart_data = {
        'cart_items': [
            {
                'id': item.id,
                'product': item.product.name,
                'quantity': item.quantity,
                'price' : item.product.price,
                'total_price' : item.get_total_price(),
                "image_url": item.product.image_url,
            }
            for item in cart_items
        ],
        'total_price': total_price
    } 
    
    return JsonResponse(cart_data)

#Add to Cart
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Keyboard, id=product_id)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            cart, created = Cart.objects.get_or_create(user=None)
            
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
            
        return JsonResponse({'message': 'Item added to cart successfully'})
    
#Remove from Cart
@csrf_exempt
def remove_from_cart(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart'})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)

#Updating Quantity of products
@csrf_exempt
def update_quantity(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = int(data.get("quantity", 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
        return JsonResponse({"success": True}, status=200)
    
#Clearing cart
@csrf_exempt
def clear_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(user=None).first()
            
        if cart:
            cart.items.all().delete()
        
        return JsonResponse({"message": "Cart cleared successfully"})
