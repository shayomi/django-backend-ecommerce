from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Art.forms import ItemForm, CheckoutForm
from django.urls import reverse_lazy
from .models import Item, OrderItem, Order, BillingAddress
from django.views.generic import (TemplateView, UpdateView,
                                  ListView, DetailView, CreateView,
                                  DeleteView, View)


# Create your views here.


class ItemListView(ListView):

    model = Item
    paginate_by = 10
    template_name = "item_list.html"

    def get_queryset(self):
        return Item.objects.all()

class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request, 'Art/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("/")





class ItemDetailView(DetailView):
    model = Item

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request, "Art/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or none)
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country  = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                #same_shipping_address = form.cleaned_data.get('same_shipping_address')
                #save_info = form.cleaned_data.get('save_info')
                payment_options = form.cleaned_data.get('payment_options')
                billing_address=BillingAddress(
                    user =self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country = country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address=billing_address
                order.save()
                return redirect('checkout')

            messages.warning(self.request, "failed checkout")
            return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("order_summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment.html")


class CreateItemView( CreateView):

    redirect_field_name = 'Art/item_list.html'
    form_class = ItemForm
    model = Item

def item_publish(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.publish()
    return redirect('item_detail', pk=item.pk)


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(item = item,
                 user = request.user, ordered=False)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # checking if the other item is in the order
        if order.items.filter(item__pk = item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated in your cart.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect('item_detail',  pk=pk)
    else:
        ordered_date = timezone.now()
        order=Order.objects.create(user=request.user,
                                    ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('item_detail',  pk=pk)
    return redirect('item_detail',  pk=pk)

@login_required
def add_single_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(item = item,
                 user = request.user, ordered=False)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # checking if the other item is in the order
        if order.items.filter(item__pk = item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated in your cart.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect('order_summary')
    else:
        ordered_date = timezone.now()
        order=Order.objects.create(user=request.user,
                                    ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('order_summary')
    return redirect('order_summary')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user = request.user,
                                     ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # checking if the other item is in the order
        if order.items.filter(item__pk = item.pk).exists():
            order_item =  OrderItem.objects.filter(item = item,
                         user = request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect('order_summary')
        else:
            #add a message saying the order does not contain the selected item
            messages.info(request, "This item was not in your cart.")
            return redirect('item_detail',  pk=pk)
    else:
        #add a messgae user doesnt have an order
        messages.info(request, "You do not have an active order.")
        return redirect('item_detail',  pk=pk)
    return redirect('item_detail',  pk=pk)


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user = request.user,
                                     ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # checking if the other item is in the order
        if order.items.filter(item__pk = item.pk).exists():
            order_item =  OrderItem.objects.filter(item = item,
                         user = request.user, ordered=False)[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)


            messages.info(request, "This item quantity was updated.")
            return redirect('order_summary')
        else:
            #add a message saying the order does not contain the selected item
            messages.info(request, "This item was not in your cart.")
            return redirect('item_detail',  pk=pk)
    else:
        #add a messgae user doesnt have an order
        messages.info(request, "You do not have an active order.")
        return redirect('item_detail',  pk=pk)
    return redirect('item_detail',  pk=pk)
