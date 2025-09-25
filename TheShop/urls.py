"""
URL configuration for TheShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .settings import MEDIA_URL, MEDIA_ROOT

from users.views import (goods_list,
                         goods_detail,
                         cart,
                         add_to_cart,
                         order,
                         order_detail,
                         auth_site,
                         )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth_site),
    path('goods/', goods_list, name='goods_list'),
    path('goods/<int:customer_id>/<int:pk>/', goods_detail, name='goods_detail'),
    path('cart/<int:customer_id>/', cart, name='cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('order/', order, name='order'),
    path('order/<int:customer_id>/', order, name='order'),
    path('order/<int:customer_id>/<int:order_id>/', order_detail, name='order_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)