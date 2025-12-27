from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('get_cart/', views.get_cart, name='get_to_cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
]