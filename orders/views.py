from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def cart(request):
    return render(request, 'orders/cart.html')


@login_required
def order_list(request):
    return render(request, 'orders/order_list.html')