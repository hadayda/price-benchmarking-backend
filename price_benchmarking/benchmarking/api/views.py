
import django.db.models
import rest_framework.views
import rest_framework.generics
import rest_framework.response
import rest_framework.status
import rest_framework.permissions
from django.db.models import Subquery

from . import serializers
from .. import rates_parsers
from .. import models
from price_benchmarking import mixins


class UploadUserRatesAPIView(rest_framework.generics.CreateAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]

    serializer_class = serializers.UserRateUploadSerializer
    queryset = models.UserMarketRates.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = mixins.parse_xlxs(file_url=serializer.validated_data['file'])
        user_rates_parser = rates_parsers.UserRatesParser(data)
        user_rates = user_rates_parser.parse()
        if not user_rates:
            return rest_framework.response.Response(user_rates_parser.errors, status=rest_framework.status.HTTP_400_BAD_REQUEST)

        for user_rate in user_rates:
            user_rate['user'] = request.user.pk
        user_rate_serializer = serializers.UserMarketRateSerializer(data=user_rates, many=True)
        user_rate_serializer.is_valid(raise_exception=True)
        self.perform_create(user_rate_serializer)
        return rest_framework.response.Response(
            user_rate_serializer.data, status=rest_framework.status.HTTP_201_CREATED
        )


class UserPotentialSavingAPIVIew(rest_framework.generics.ListAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    serializer_class = serializers.UserPotentialSavingSerializer

    def get_queryset(self):
        aggregated_data_subquery = models.AggregatedMarketRates.objects.filter(
            origin=django.db.models.OuterRef('origin'),
            destination=django.db.models.OuterRef('destination'),
            effective_on=django.db.models.OuterRef('effective_on')
        )
        return self.request.user.market_rates.values(
            'origin', 'destination', 'effective_on'
        ).order_by('effective_on').annotate(
            user_price=django.db.models.Sum('price'),
            user_annual_volume=django.db.models.Sum('annual_volume'),
            max_price=Subquery(aggregated_data_subquery.values('max_price')[:1]),
            min_price=Subquery(aggregated_data_subquery.values('min_price')[:1]),
            median_price=Subquery(aggregated_data_subquery.values('median_price')[:1]),
            percentile_90_price=Subquery(aggregated_data_subquery.values('percentile_90_price')[:1]),
            percentile_10_price=Subquery(aggregated_data_subquery.values('percentile_10_price')[:1]),
        ).values(
            'origin', 'destination', 'effective_on', 'user_price', 'user_annual_volume', 'max_price',
            'min_price', 'median_price', 'percentile_90_price', 'percentile_10_price',
        )