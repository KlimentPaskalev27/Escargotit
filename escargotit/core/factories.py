import factory
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import *

#https://factoryboy.readthedocs.io/en/stable/orms.html 

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')

class AdminUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdminUser

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    business_name = factory.Faker('company')
    company_tax_code = factory.Faker('ssn')
    can_create_snailbed = True

class EmployeeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeUser

    user = factory.SubFactory(UserFactory)
    admin = factory.SubFactory(AdminUserFactory)
    can_create_snailbed = False

class SnailBedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SnailBed

    bed_name = factory.Faker('word')
    user = factory.SubFactory(AdminUserFactory)
    snail_amount = factory.Faker('random_int', min=0, max=1000)
    hatch_rate = None
    mortality_rate = None
    maturity_rate = None

class SnailHatchRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SnailHatchRate

    snail_bed = factory.SubFactory(SnailBedFactory)
    preexisting_snail_amount = factory.Faker('random_int', min=0, max=1000)
    newly_hatched_snails = factory.Faker('random_int', min=0, max=100)
    datetime = factory.Faker('date_time_this_decade')

class SnailMortalityRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SnailMortalityRate

    snail_bed = factory.SubFactory(SnailBedFactory)
    preexisting_snail_amount = factory.Faker('random_int', min=0, max=1000)
    expired_snail_amount = factory.Faker('random_int', min=0, max=100)
    datetime = factory.Faker('date_time_this_decade')

class TimeTakenToMatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeTakenToMature

    snail_bed = factory.SubFactory(SnailBedFactory)
    snail_hatched = factory.Faker('date_time_this_decade')
    snail_matured = factory.Faker('date_time_this_decade')
    snails_matured_count = factory.Faker('random_int', min=0, max=1000)

class SnailFeedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SnailFeed

    snail_bed = factory.SubFactory(SnailBedFactory)
    consumed_on = factory.Faker('date_time_this_decade')
    grams_feed_given = factory.Faker('random_int', min=0, max=1000)