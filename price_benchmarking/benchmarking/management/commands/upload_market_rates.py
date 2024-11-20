import logging

import django.core.management.base
import django.core.paginator

from ... import rates_parsers
from ... import models
from price_benchmarking import  mixins

logger = logging.getLogger(__name__)


class Command(django.core.management.base.BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file-url', type=str, required=False)
        parser.add_argument('--file-path', type=str, required=False)

    def handle(self, *args, **options):
        file_path = options.get('file_path')
        file_url = options.get('file_url')
        if not any([file_path, file_url]):
            logger.error('--file-path or --file-url need to be provided')
            return
        logger.info('Reading Market Rates file')
        csv_data = self.read_csv(file_path, file_url)
        market_rates_parser = rates_parsers.MarketRatesParser(csv_data)
        market_rates_data = market_rates_parser.parse()
        if not market_rates_data:
            logger.error(market_rates_parser.errors)
        market_rates_objects = [models.MarketRates(**market_rate) for market_rate in market_rates_data]
        paginator = django.core.paginator.Paginator(market_rates_objects, 1000)
        total_count = 0
        for page_num in paginator.page_range:
            page = paginator.page(page_num)
            objects = models.MarketRates.objects.bulk_create(page.object_list, batch_size=100)
            total_count += len(objects)
            logger.info(f'{total_count} market rates were created')

    def read_csv(self, file_path='', file_url=''):
        return mixins.parse_xlxs(file_path, file_url)