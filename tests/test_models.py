from django.test import TestCase
from users.models import Goods, Customers, Cart
from users.views import add_to_cart

"""
Прошу прощения, с автотестами я не разобрался. Обучающий урок меня не обучил, там просто показывают, как в кучу кода
дописывают и запускают что-то и радуются какому-то результату (я даже на паузе не смог рассмотреть, где этот результат).
Полагаю, использование тестов я буду изучать отдельно, пока же обошелся ручными тестами.
Пример из задания не подходит, так как у меня иначе хранятся складские остатки и я не понимаю, что делает этот шматок
кода ниже. 
"""
class ProductTestCase(TestCase):
    def test_stock_balance(self):
        product = Goods.objects.create(name='Test Product', price=10, quantity=5)
        customer = Customers.objects.create(name='Test Customer', email='test@example.com')
        cart = Cart(user = customer)
        add_to_cart(cart, product, quantity=3)
        self.assertEqual(product.quantity, 7)
        self.assertEqual(cart.items, (product, 3))
        with self.assertRaises(Exception):
            add_to_cart(cart, product, quantity=8)
        self.assertEqual(product.quantity, 7)
        self.assertEqual(cart.items, (product, 3))

