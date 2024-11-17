# how to create the filter in django
from django import template

register = template.Library()


# it gave the particular product is in cart or not
@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
        # if id == product.id:
            return True
    return False


# it gave the number of quantity of a particular product
@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id) # show the quantity of particular items
    return 0

# it gave the product_price * quantity
@register.filter(name='price_total')
def price_total(product , cart):
    return product.price*cart_quantity(product, cart)

# it give total of prices
@register.filter(name='subtotal')
def subtotal(products, cart):
    total = 0
    for i in products:
        quantity = cart_quantity(i, cart)
        total += quantity*i.price
    return total
@register.filter(name='multiply')
def multiply(num1,num2):
    return num1*num2