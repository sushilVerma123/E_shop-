from django.contrib import admin
from django.urls import path
from .views import index, signup, Login, logout, cart,CheckOut,Orders
from store.middleware.auth import auth_middleware
urlpatterns = [
    path('', index, name='homepage'),
    path('signup', signup),
    # path('Login', login)    # when we use function oriented
    path('Login', Login.as_view(), name='login'),  # using class
    path('Logout', logout),
    path('cart', cart, name='cart'),
    path('check-out', CheckOut, name='checkout'),
    path('order', auth_middleware(Orders), name='order'),


]
