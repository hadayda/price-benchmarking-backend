import django.db.models

class RateBase(django.db.models.Model):
    origin = django.db.models.CharField(max_length=250, db_index=True)
    destination = django.db.models.CharField(max_length=250, db_index=True)
    effective_on = django.db.models.DateField()

    class Meta:
        abstract = True

class MarketRates(RateBase):
    price = django.db.models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Market Rate'
        verbose_name_plural = 'Market Rates'


class AggregatedMarketRates(RateBase):
    min_price = django.db.models.DecimalField(max_digits=10, decimal_places=2)
    max_price = django.db.models.DecimalField(max_digits=10, decimal_places=2)
    median_price = django.db.models.DecimalField(max_digits=10, decimal_places=2)
    percentile_90_price = django.db.models.DecimalField(max_digits=10, decimal_places=2)
    percentile_10_price = django.db.models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Aggregated Market Rate'
        verbose_name_plural = 'Aggregated Market Rates'
        unique_together = ('origin', 'destination', 'effective_on')


class UserMarketRates(RateBase):
     user = django.db.models.ForeignKey('accounts.User', on_delete=django.db.models.PROTECT, related_name='market_rates')
     expired_on = django.db.models.DateField()
     price = django.db.models.DecimalField(max_digits=10, decimal_places=2)
     annual_volume = django.db.models.DecimalField(max_digits=10, decimal_places=2)

     class Meta:
         verbose_name = 'User Market Rate'
         verbose_name_plural = 'User Market Rates'