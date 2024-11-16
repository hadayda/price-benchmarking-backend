import django.core.management
from ... import  tasks


class Command(django.core.management.base.BaseCommand):
    def handle(self, *args, **options):
        tasks.calculate_market_rates_aggregated_data()
