from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Goods, Cart
from .forms import CartForm

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
	cart = Cart.objects.all().filter(Q(customer_id=customer_id))
	context = {'cart': cart}
	return render(request, 'cart.html', context)

def add_to_cart(request):
	if request.method == 'POST':
		form = CartForm(request.POST)
		if form.is_valid():
			product = form.cleaned_data['product']
			quantity = form.cleaned_data['quantity']
			cart, created = Cart.objects.get_or_create(customer_id=1) #user=request.user
			cart.goods_id = product
			cart.goods_cnt = quantity
			cart.save()

		return redirect('cart')
	else:
		form = CartForm()
		return render(request, 'add_to_cart.html', {'form': form})