import numpy

import django.db.models
import django.db.models.expressions
import django.db.models.functions
from django.contrib.postgres.aggregates import ArrayAgg

from . import models


'''
    This task should be done run in a cron job every 1 or 2 hours to refresh the aggregated data.
    And FYI, All of this could've been done much cleaner and easier if it wasn't for MySQL, Postgresql is way better.
'''
def calculate_market_rates_aggregated_data():
    aggregated_queryset = models.MarketRates.objects.values(
        'origin', 'destination', 'effective_on'
    ).order_by('effective_on').annotate(
        max_price=django.db.models.Max('price'),
        min_price=django.db.models.Min('price'),
        ordered_prices=ArrayAgg(
            django.db.models.functions.Cast(
                'price', output_field=django.db.models.FloatField()
            ), ordering='price'
        ),
    ).values('origin', 'destination', 'effective_on', 'max_price', 'min_price', 'ordered_prices')
    for data in aggregated_queryset:
        ordered_prices = data['ordered_prices']
        median_price = numpy.percentile(ordered_prices, 50)
        percentile_90_price = numpy.percentile(ordered_prices, 90)
        percentile_10_price = numpy.percentile(ordered_prices, 10)
        models.AggregatedMarketRates.objects.update_or_create(
            destination=data['destination'], origin=data['origin'], effective_on=data['effective_on'],
            defaults={
                'max_price': data['max_price'],
                'min_price': data['min_price'],
                'median_price': median_price,
                'percentile_90_price': percentile_90_price,
                'percentile_10_price': percentile_10_price,
            }
        )
