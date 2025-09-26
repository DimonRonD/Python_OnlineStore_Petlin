from django.core.management.base import BaseCommand
from users.models import Warehouse, Goods
import json

class Command(BaseCommand):
    help = 'Обновляет остатки товаров в базе данных из файла residue_data.json'

    def handle(self, *args, **options):
        with open('residue_data.json', encoding='utf-8') as file:
            data = json.load(file)

        for entry in data:
            try:
                goods = Goods.objects.get(goods_id=entry['goods_id'])
                warehouse, created = Warehouse.objects.update_or_create(
                    goods_id=goods,
                    defaults={'goods_cnt': entry['goods_quantity']}
                )

            except Goods.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Товар с ID={entry['goods_id']} не найден"))
                continue

        self.stdout.write(self.style.SUCCESS('Остатки товаров успешно обновлены.'))