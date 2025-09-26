from django.core.management.base import BaseCommand
from users.models import Warehouse
import json

class Command(BaseCommand):
    help = 'Экспортирует остатки товаров в JSON файл.'

    def handle(self, *args, **options):
        warehouses = Warehouse.objects.all()
        residue_data = [
            {
                'goods_id': w.goods_id.goods_id,
                'goods_name': w.goods_id.goods_name,
                'goods_brand': w.goods_id.brand_id.brand_name,
                'goods_category': w.goods_id.goods_category_id.category_name,
                'goods_quantity': w.goods_cnt
            }
            for w in warehouses
        ]

        with open('residue_data.json', 'w', encoding='utf-8') as file:
            json.dump(residue_data, file, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Остатки товаров успешно экспортированы.'))