from django.shortcuts import render, redirect ,HttpResponseRedirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order

import re
#  this is use for password hashing
from django.contrib.auth.hashers import make_password, check_password
from django.views import View

# Create your views here.
def index(request):
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        # request.session.clear() # this is clear the session
        # request.session.get('cart').clear()  # this is clear the only cart

        # it get all the categories from the database
        categories = Category.get_all_categories()

        #  get the category from the index.html
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        data = {
            'products': products,
            'categories': categories,
            'email': request.session.get('email')
        }
        # print the session stor email
        # print('your email is: ', request.session.get('email'))
        return render(request, 'index.html', data)
    else:
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('homepage')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    #  post method
    else:
        # access the data
        email = request.POST.get('email')
        password = request.POST.get('password')

        # create the object of Customer class
        customer = Customer(email=email, password=password)

        # validation
        error_message = None
        if len(password) < 8:
            error_message = 'minimum length of password is 8'
        # if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@gmail.com", email):
            error_message = 'invalid email'

        # check the inter email already signup or not
        if customer.isExists():
            error_message = 'This email already registered'

        # save the data
        if not error_message:
            # this is use for password hashing
            customer.password = make_password(customer.password)

            # we call the function in customer which save the data
            customer.register()

            # method to redirect the another page
            # return redirect('http://127.0.0.1:8000/')
            return redirect('homepage')

        else:
            return render(request, 'signup.html', {'error': error_message})


# implement the login function without the help of class
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     else:
#         error_message = None
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         customer = Customer.get_customer_by_email(email)
#         if customer and check_password(password,customer.password):
#             return redirect('homepage')
#         else:
#             error_message = 'Email or Password invalid !!'
#         return render(request, 'login.html', {'error': error_message})


# with the help of class
class Login(View):
    return_Url=None
    def get(self, request):
        Login.return_Url=request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        error_message = None
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check the email is exist in data base or not
        customer = Customer.get_customer_by_email(email)

        if customer and check_password(password, customer.password):
            # use session
            request.session['customer_id'] = customer.id
            request.session['email'] = customer.email
            if Login.return_Url:
                return HttpResponseRedirect(Login.return_Url)
            else:
                Login.return_Url=None
                return redirect('homepage')
        else:
            error_message = 'Email or Password invalid !!'
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


def cart(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart']={}
    if request.method == 'GET':
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        cart_detail = {
            'products':products,
            'email':request.session.get('email')
        }
    return render(request, 'cart.html',cart_detail)


def CheckOut(request):
    if request.method == 'POST':
        address= request.POST.get('address')
        phone=request.POST.get('Phone')

        customer= request.session.get('customer_id')
        cart = request.session.get('cart')

        products=Product.get_products_by_id(list(cart.keys()))
        for product in products:
            order = Order(customer = Customer(id=customer),
                          product = product,
                          price= product.price,
                          quantity= cart.get(str(product.id)),
                          address= address,
                          phone=phone
            )
            order.placeOrder()
        request.session['cart']={}
        return redirect('cart')


def Orders(request):
    if request.method == 'GET':
        customer_id = request.session.get('customer_id')
        detail= Order.get_all_order_of_customer(customer_id)
        customer_detail={
            'details':detail,
            'email':request.session.get('email')
        }
    return render(request, 'orders.html',customer_detail)

