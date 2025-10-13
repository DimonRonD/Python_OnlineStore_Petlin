from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, F
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .models import Good, Cart, Warehouse, Order, OrderGood, OrderStatus, Status, GoodCategory
from .forms import CartForm, OrderForm, ToCartForm, LoginForm, RegisterForm


# Create your views here.
@login_required
def goods_list(request):
    context = {
        'categoryes': GoodCategory.objects.all()
    }
    return render(request, 'goods_list.html', context)

def goods_detail(request, pk):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    form = ToCartForm()
    goods = Good.objects.get(goods_id=pk)
    context = {'goods': goods,
               'form': form,
               }
    return render(request, 'goods_detail.html', context)

def cart(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    customer_id = request.user.id
    form = OrderForm(initial={'customer_id': customer_id})
    cart = Cart.objects.all().filter(Q(customer_id=customer_id))
    total_cost = sum(item.goods_id.goods_price * item.goods_cnt for item in cart)
    context = {'cart': cart,
               'form': form,
               'total_cost': total_cost,}
    return render(request, 'cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            customer = request.user
            if quantity != 0:
                cart, create = Cart.objects.get_or_create(customer_id=customer, goods_id=product)
                cart.goods_cnt = quantity
                cart.save()
            else:
                cart = Cart.objects.get(customer_id=customer, goods_id=product)
                cart.delete()

        return redirect(f'/cart/')
    else:
        form = CartForm()
        return render(request, 'add_to_cart.html', {'form': form})

def order(request):
    customer = request.user
    if request.method == 'POST':
        cart = Cart.objects.filter(customer_id=customer)
        order, create = Order.objects.get_or_create(customer_id=customer, order_date=datetime.now())
        for item in cart:
            """
                Вот тут я проверяю наличие товара на складе и что товара хватает для заказа
            """
            wh_cnt = Warehouse.objects.get(goods_id = item.goods_id)
            if item.goods_cnt <= wh_cnt.goods_cnt:
                """
                    Здесь уменьшаем количество товара на складе
                """
                wh_cnt.goods_cnt = wh_cnt.goods_cnt - item.goods_cnt
                wh_cnt.save()
                order_goods = OrderGood.objects.create(order_id=order, goods_id=item.goods_id, goods_cnt = item.goods_cnt)
                order_goods.save()
                item.delete()
                status = Status.objects.get(pk=1)
                order_status, create = OrderStatus.objects.get_or_create(order_id=order, sdate=datetime.now(), edate ='2099-01-01', order_status_id=status)
                order_status.save()

                new_order = OrderGood.objects.all().filter(order_id=order)
                orders = Order.objects.all().filter(customer_id=customer).order_by('-order_date')
                order_statuses = OrderStatus.objects.select_related('order_status_id').all().filter(
                    Q(edate='2099-01-01'))

                total_prices = {}
                for order in orders:
                    total_price = OrderGood.objects.filter(
                        order_id=order
                    ).aggregate(total=Sum(F('goods_cnt') * F('goods_id__goods_price')))['total'] or 0
                    total_prices[order.order_id] = total_price

                order_goods = OrderGood.objects.filter(order_id__in=orders).select_related('goods_id')
                context = {'orders': orders,
                           'order_goods': order_goods,
                           'total_prices': total_prices,
                           'new_order': new_order,
                           'order_statuses': order_statuses, }

                return render(request, 'order.html', context)

            else:
                """
                    Вот тут ответ, что количества товара недостаточно
                """
                order.delete()
                orders = Order.objects.all().filter(customer_id=customer).order_by('-order_date')
                order_statuses = OrderStatus.objects.select_related('order_status_id').all().filter(
                    Q(edate='2099-01-01'))

                total_prices = {}
                for order in orders:
                    total_price = OrderGood.objects.filter(
                        order_id=order
                    ).aggregate(total=Sum(F('goods_cnt') * F('goods_id__goods_price')))['total'] or 0
                    total_prices[order.order_id] = total_price

                order_goods = OrderGood.objects.filter(order_id__in=orders).select_related('goods_id')
                answer = "Вы хотите заказать товара больше, чем есть на складе"
                context = {'orders': orders,
                           'order_goods': order_goods,
                           'total_prices': total_prices,
                           'answer': answer,
                           'order_statuses': order_statuses, }

                return render(request, 'order.html', context)
    else:
        orders = Order.objects.all().filter(customer_id=customer).order_by('-order_date')
        order_statuses = OrderStatus.objects.select_related('order_status_id').all().filter(Q(edate='2099-01-01'))
        total_prices = {}
        for order in orders:
            total_price = OrderGood.objects.filter(
                order_id=order
            ).aggregate(total=Sum(F('goods_cnt') * F('goods_id__goods_price')))['total'] or 0

            total_prices[order.order_id] = total_price
        order_goods = OrderGood.objects.filter(order_id__in=orders).select_related('goods_id')
        context = {'orders': orders,
                   'order_goods': order_goods,
                   'total_prices': total_prices,
                   'order_statuses': order_statuses,}

        return render(request, 'order.html', context)



def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_statuses = OrderStatus.objects.select_related('order_status_id').filter(Q(order_id=order))
    context = {'order': order,
               'order_statuses': order_statuses,
               }
    return render(request, 'order_details.html', context)


def auth_site(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = authenticate(request, username=form.cleaned_data["email"], password=form.cleaned_data["password"])
                login(request, user)
                redirect_url = reverse("goods_list")
                return HttpResponseRedirect(redirect_url)
            except Exception as e:
                return HttpResponse(f"Нихера не вышло {e}")
        else:
            return HttpResponse(f"Нихера не вышло")
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'auth.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        redirect_url = reverse("redirect")
        return HttpResponseRedirect(redirect_url)
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)
