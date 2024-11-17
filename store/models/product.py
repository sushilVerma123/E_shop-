from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200, default="", null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')


    @staticmethod
    # it serve all the products
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    # it serve the all product related to this  categoryid
    def get_all_products_by_categoryid(category_id=None):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)  # it give all the detail about the product and (id__in) means we pass the list of products id