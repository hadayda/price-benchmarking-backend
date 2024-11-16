# Generated by Django 5.1.3 on 2024-11-15 23:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(db_index=True, max_length=250)),
                ('destination', models.CharField(db_index=True, max_length=250)),
                ('effective_on', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Market Rate',
                'verbose_name_plural': 'Market Rates',
            },
        ),
        migrations.CreateModel(
            name='AggregatedMarketRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(db_index=True, max_length=250)),
                ('destination', models.CharField(db_index=True, max_length=250)),
                ('effective_on', models.DateField()),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('median_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('percentile_90_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('percentile_10_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Aggregated Market Rate',
                'verbose_name_plural': 'Aggregated Market Rates',
                'unique_together': {('origin', 'destination', 'effective_on')},
            },
        ),
        migrations.CreateModel(
            name='UserMarketRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(db_index=True, max_length=250)),
                ('destination', models.CharField(db_index=True, max_length=250)),
                ('effective_on', models.DateField()),
                ('expire_on', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('annual_volume', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='market_rates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Market Rate',
                'verbose_name_plural': 'User Market Rates',
            },
        ),
    ]