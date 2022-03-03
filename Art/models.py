from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django_countries.fields import CountryField, countries

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length = 200)
    item_image = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length = 500)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={'pk':self.pk})

    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={'pk':self.pk})

    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={'pk':self.pk})



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True,)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    billing_address = models.ForeignKey('BillingAddress', on_delete = models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
