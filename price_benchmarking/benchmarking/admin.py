import django.contrib.admin

from . import models

@django.contrib.admin.register(models.MarketRates)
class MarketRatesAdmin(django.contrib.admin.ModelAdmin):
    pass


@django.contrib.admin.register(models.AggregatedMarketRates)
class AggregatedMarketRatesAdmin(django.contrib.admin.ModelAdmin):
    pass


@django.contrib.admin.register(models.UserMarketRates)
class UserMarketRatesAdmin(django.contrib.admin.ModelAdmin):
    pass
