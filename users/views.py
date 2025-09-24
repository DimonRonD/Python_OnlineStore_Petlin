from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Goods, Cart, Customers
from .forms import CartForm, OrderForm

# Create your views here.
def goods_list(request):
	goods = Goods.objects.all()
	context = {'goods': goods}
	return render(request, 'goods_list.html', context)

def goods_detail(request, pk):
	goods = Goods.objects.get(goods_id=pk)
	context = {'goods': goods}
	return render(request, 'goods_detail.html', context)

def cart(request, customer_id):
	if request.method == 'POST':
		pass
	else:
		form = OrderForm()
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
		form = OrderForm(request.POST)