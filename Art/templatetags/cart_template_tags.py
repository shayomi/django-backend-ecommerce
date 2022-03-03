from django import template
from Art.models import Order
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='cart_item_count')
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
