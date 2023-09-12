from rest_framework import serializers
from .models import *

class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = '__all__'

class SnailHatchRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnailHatchRate
        fields = '__all__'

    # Define a custom method to serialize SnailHatchRate objects
    def to_representation(self, instance):
        representation = {
            'preexisting_snail_amount': instance.preexisting_snail_amount,
            'newly_hatched_snails': instance.newly_hatched_snails,
            'hatch_rate_percentage': instance.hatch_rate_percentage,
            'datetime': instance.datetime,
        }
        return representation

class SnailMortalityRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnailMortalityRate
        fields = '__all__'

    # Define a custom method to serialize SnailHatchRate objects
    def to_representation(self, instance):
        representation = {
            'preexisting_snail_amount': instance.preexisting_snail_amount,
            'expired_snail_amount': instance.expired_snail_amount,
            'mortality_rate_percentage': instance.mortality_rate_percentage,
            'datetime': instance.datetime,
        }
        return representation

class SnailFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnailFeed
        fields = '__all__'

    # Define a custom method to serialize SnailHatchRate objects
    def to_representation(self, instance):
        representation = {
            'consumed_on': instance.consumed_on,
            'grams_feed_given': instance.grams_feed_given,
        }
        return representation

class TimeTakenToMatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTakenToMature
        fields = '__all__'

    # Define a custom method to serialize SnailHatchRate objects
    def to_representation(self, instance):
        representation = {
            'snail_hatched': instance.snail_hatched,
            'snail_matured': instance.snail_matured,
            'snails_matured_count': instance.snails_matured_count,
            'days_to_mature': instance.days_to_mature,
            'period': instance.period,
            'maturity_percentage': instance.maturity_percentage,
        }
        return representation

class SnailBedSerializer(serializers.ModelSerializer):
    hatch_rates = SnailHatchRateSerializer(many=True, read_only=True)
    mortality_rates = SnailMortalityRateSerializer(many=True, read_only=True)
    feed_history = SnailFeedSerializer(many=True, read_only=True)
    maturity_history = TimeTakenToMatureSerializer(many=True, read_only=True)

    class Meta:
        model = SnailBed
        fields = '__all__'


class SpecificSnailBedSerializer(serializers.ModelSerializer):
    hatch_rates = SnailHatchRateSerializer(many=True, read_only=True)
    mortality_rates = SnailMortalityRateSerializer(many=True, read_only=True)
    feed_history = SnailFeedSerializer(many=True, read_only=True)
    maturity_history = TimeTakenToMatureSerializer(many=True, read_only=True)

    snail_hatch_rates = serializers.SerializerMethodField()
    snail_mortality_rates = serializers.SerializerMethodField()
    snail_feed_history = serializers.SerializerMethodField()
    snail_maturity_history = serializers.SerializerMethodField()

    class Meta:
        model = SnailBed
        fields = '__all__'

    # Define a custom method to serialize SnailHatchRate objects for SnailBed
    def get_snail_hatch_rates(self, obj):
        # Serialize related SnailHatchRate objects for the SnailBed
        hatch_rates = SnailHatchRate.objects.filter(snail_bed=obj)
        return SnailHatchRateSerializer(hatch_rates, many=True).data

    def get_snail_mortality_rates(self, obj):
        mortality_rates = SnailMortalityRate.objects.filter(snail_bed=obj)
        return SnailMortalityRateSerializer(mortality_rates, many=True).data

    def get_snail_feed_history(self, obj):
        feed_history = SnailFeed.objects.filter(snail_bed=obj)
        return SnailFeedSerializer(feed_history, many=True).data

    def get_snail_maturity_history(self, obj):
        maturity_history = TimeTakenToMature.objects.filter(snail_bed=obj)
        return TimeTakenToMatureSerializer(maturity_history, many=True).data