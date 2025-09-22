from django.shortcuts import render
from .models import Goods

# Create your views here.
def goods_list(request):
	goods = Goods.objects.all()
	context = {'goods': goods}
	return render(request, 'goods_list.html', context)

def goods_detail(request, pk):
	goods = Goods.objects.get(goods_id=pk)
	context = {'goods': goods}
	return render(request, 'goods_detail.html', context)