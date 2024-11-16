import rest_framework.serializers
import rest_framework.authtoken.models

from .. import  models


class UserRateUploadSerializer(rest_framework.serializers.Serializer):
    file = rest_framework.serializers.URLField()


class UserMarketRateSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = models.UserMarketRates
        fields = ['origin', 'destination', 'effective_on', 'expired_on', 'price', 'annual_volume', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].write_only = True


class UserPotentialSavingSerializer(rest_framework.serializers.Serializer):
    origin = rest_framework.serializers.CharField()
    destination = rest_framework.serializers.CharField()
    effective_on = rest_framework.serializers.DateField()
    user_price = rest_framework.serializers.FloatField()
    user_annual_volume = rest_framework.serializers.FloatField()
    max_price = rest_framework.serializers.FloatField()
    min_price = rest_framework.serializers.FloatField()
    median_price = rest_framework.serializers.FloatField()
    percentile_90_price = rest_framework.serializers.FloatField()
    percentile_10_price = rest_framework.serializers.FloatField()
    potential_savings_max_price = rest_framework.serializers.SerializerMethodField()
    potential_savings_min_price = rest_framework.serializers.SerializerMethodField()
    potential_savings_median_price = rest_framework.serializers.SerializerMethodField()
    potential_savings_percentile_90_price = rest_framework.serializers.SerializerMethodField()
    potential_savings_percentile_10_price = rest_framework.serializers.SerializerMethodField()

    def get_potential_savings_max_price(self, obj):
        return (obj['max_price'] - obj['user_price']) * obj['user_annual_volume']

    def get_potential_savings_min_price(self, obj):
        return (obj['min_price'] - obj['user_price']) * obj['user_annual_volume']

    def get_potential_savings_median_price(self, obj):
        return (obj['median_price'] - obj['user_price']) * obj['user_annual_volume']

    def get_potential_savings_percentile_90_price(self, obj):
        return (obj['percentile_90_price'] - obj['user_price']) * obj['user_annual_volume']

    def get_potential_savings_percentile_10_price(self, obj):
        return (obj['percentile_10_price'] - obj['user_price']) * obj['user_annual_volume']
