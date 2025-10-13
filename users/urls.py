from django.urls import path

from . import views

urlpatterns = [
    path("", views.auth_site),
    path("redirect", views.auth_site, name="redirect"),
    path('goods/', views.goods_list, name='goods_list'),
    path('goods/<int:pk>/', views.goods_detail, name='goods_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('order/', views.order, name='order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register', views.register, name='register'),
]
