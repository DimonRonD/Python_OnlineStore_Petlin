from datetime import datetime
from itertools import product

from django.db.models import Q, Sum, F
from django.shortcuts import render, redirect
from .models import Goods, Cart, Customers, Warehouse, Orders, Order_goods, Order_status, Status
from .forms import CartForm, OrderForm, ToCartForm

# Create your views here.
def goods_list(request):
	goods = Goods.objects.all()
	context = {'goods': goods}
	return render(request, 'goods_list.html', context)

def goods_detail(request, pk):
	if request.method == 'POST':
		pass
	else:
		form = ToCartForm()
		goods = Goods.objects.get(goods_id=pk)
		context = {'goods': goods, 'form': form,}
		return render(request, 'goods_detail.html', context)

def cart(request, customer_id):
	if request.method == 'POST':
		pass
	else:
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
		customer = Customers.objects.get(pk=1)
		if form.is_valid():
			product = form.cleaned_data['product']
			quantity = form.cleaned_data['quantity']
			if quantity != 0:
				cart, create = Cart.objects.get_or_create(customer_id=customer, goods_id=product)
				cart.goods_cnt = quantity
				cart.save()
			else:
				cart = Cart.objects.get(customer_id=customer, goods_id=product)
				cart.delete()

		return redirect('/cart/1/')
	else:
		form = CartForm()
		return render(request, 'add_to_cart.html', {'form': form})

def order(request):
	if request.method == 'POST':
		customer_id = request.POST['customer_id']
		customer = Customers.objects.get(pk=customer_id)
		cart = Cart.objects.all().filter(Q(customer_id=customer.customer_id))
		order, create = Orders.objects.get_or_create(customer_id=customer, order_date=datetime.now())
		for item in cart:
			wh_cnt = Warehouse.objects.get(goods_id = item.goods_id)
			print("--------------> ", item.goods_cnt, wh_cnt.goods_cnt)
			if item.goods_cnt <= wh_cnt.goods_cnt:
				print("--------------> ", item.goods_cnt, wh_cnt.goods_cnt)
				wh_cnt.goods_cnt = wh_cnt.goods_cnt - item.goods_cnt
				wh_cnt.save()
				order_goods = Order_goods.objects.create(order_id=order, goods_id=item.goods_id, goods_cnt = item.goods_cnt)
				order_goods.save()
				item.delete()
			else:
				return render(request, 'order.html', {'answer':'Quantity dont match'})
	else:
		customer_id = 1
		customer = Customers.objects.get(pk=customer_id)
		orders = Orders.objects.all().filter(customer_id=customer.customer_id)
		total_prices = {}
		for order in orders:
			total_price = Order_goods.objects.filter(
				order_id=order
			).aggregate(total=Sum(F('goods_cnt') * F('goods_id__goods_price')))['total'] or 0

			total_prices[order.order_id] = total_price
		# order_goods = Order_goods.objects.all().filter(order_id=order)
		order_goods = Order_goods.objects.filter(order_id__in=orders).select_related('goods_id')
		context = {'orders': orders,
				   'order_goods': order_goods,
				   'customer_id': customer.customer_id,
				   'total_prices': total_prices,}

		return render(request, 'order.html', context)


	new_order = Order_goods.objects.all().filter(order_id=order)
	orders = Orders.objects.all().filter(customer_id=customer.customer_id)
	# order_goods = Order_goods.objects.all().filter(order_id=order)
	order_goods = Order_goods.objects.filter(order_id__in=orders).select_related('goods_id')
	context = {'orders': orders,
			   'order_goods': order_goods,
			   'new_order': new_order,
			   'customer_id': customer.customer_id}

	return render(request, 'order.html', context)

