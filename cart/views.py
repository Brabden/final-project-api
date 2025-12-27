from products.models import Keyboard
from .models import Cart, CartItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
                'total_price' : item.get_total_price()
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


#------------ Login/Signup Section -----------------------

#Signup
@api_view(['POST'])
@csrf_exempt
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if User.objects.filter(username=email).exists():
        return Response({"error": "User with this email already exists"})
    
    user = User.objects.create(
        username=email,
        password=make_password(password)
    )
    return Response({"message": "Account created successfully!"}, status=status.HTTP_201_CREATED)

# Login
@api_view(['POST'])
@csrf_exempt
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(user=email, password=password)
    
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    