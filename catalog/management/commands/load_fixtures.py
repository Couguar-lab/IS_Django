from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загружает тестовые данные из фикстур (с предварительной очисткой)'

    def handle(self, *args, **options):
        self.stdout.write('Очистка старых данных...')
        call_command('flush', '--no-input')

        self.stdout.write('Загрузка категорий...')
        call_command('loaddata', 'categories.json')

        self.stdout.write('Загрузка продуктов...')
        call_command('loaddata', 'products.json')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))