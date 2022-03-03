from django.conf.urls import url
from Art import views
from .views import ItemDetailView, ItemListView, add_to_cart, OrderSummaryView, PaymentView



urlpatterns = [
    url(r'^$', views.ItemListView.as_view(), name = 'item_list'),
    url(r'^item/new/$', views.CreateItemView.as_view(), name = 'new_item'),
    url(r'^item/checkout/$', views.CheckoutView.as_view(), name = 'checkout'),
    url(r'^item/(?P<pk>\d+)$', views.ItemDetailView.as_view(), name = 'item_detail'),
    url(r'^item/(?P<pk>\d+)/publish/$', views.item_publish, name = 'item_publish'),
    url(r'^item/(?P<pk>\d+)/add_to_cart/$', views.add_to_cart, name = 'add_to_cart'),
    url(r'^item/(?P<pk>\d+)/add_single_to_cart/$', views.add_single_to_cart, name = 'add_single_to_cart'),
    url(r'^item/order_summary/$', views.OrderSummaryView.as_view(), name = 'order_summary'),
    url(r'^item/(?P<pk>\d+)/remove_from_cart/$', views.remove_from_cart, name = 'remove_from_cart'),
    url(r'^item/(?P<pk>\d+)/remove_single_item_from_cart/$', views.remove_single_item_from_cart, name = 'remove_single_item_from_cart'),
    url(r'^item/payment/<payment_options>/$', views.PaymentView.as_view(), name = 'payment')
]
