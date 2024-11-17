from django.db import models


class Customer(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=500)

    # use to save the data in sqlite
    def register(self):
        self.save()

# check the email exist or not
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False

    @staticmethod
    # check the email at login
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

