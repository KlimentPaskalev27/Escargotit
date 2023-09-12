import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from ..factories import *

# run with command:
# python manage.py test core
# must be in outer escargotit directory, children directories are core and escargotit


# sources used
#https://docs.python.org/3/library/unittest.html#assert-methods
#https://docs.djangoproject.com/en/4.2/topics/testing/overview/

class AdminUserTestCase(TestCase):
    def test_has_user(self):
        admin = AdminUserFactory()
        self.assertIsInstance(admin.user, User)

    def test_admin_user_creation(self):
        admin = AdminUserFactory()
        self.assertIsInstance(admin, AdminUser)

    def test_has_business_name(self):
        admin = AdminUserFactory()
        self.assertIsNotNone(admin.business_name)

    def test_has_company_tax_code(self):
        admin = AdminUserFactory()
        self.assertIsNotNone(admin.company_tax_code)

    def test_can_create_snailbeds(self):
        admin = AdminUserFactory()
        self.assertTrue(admin.can_create_snailbed)

class EmployeeUserTestCase(TestCase):
    def test_has_user(self):
        employee = EmployeeUserFactory()
        self.assertIsInstance(employee.user, User)

    def test_employee_creation(self):
        employee = EmployeeUserFactory()
        self.assertIsInstance(employee, EmployeeUser)

    def test_employee_has_admin(self):
        employee = EmployeeUserFactory()
        self.assertIsInstance(employee.admin, AdminUser)

    def test_cannot_create_snailbeds(self):
        employee = EmployeeUserFactory()
        self.assertFalse(employee.can_create_snailbed)

class SnailBedTestCase(TestCase):
    def test_has_user(self):
        snail_bed = SnailBedFactory()
        self.assertIsInstance(snail_bed.user, AdminUser)
    
    def test_snail_bed_creation(self):
        snail_bed = SnailBedFactory()
        self.assertIsInstance(snail_bed, SnailBed)

    def test_snail_bed_default_name_generation(self):
        snail_bed = SnailBedFactory(bed_name=None)
        self.assertIsNotNone(snail_bed.bed_name)
        self.assertTrue(snail_bed.bed_name.startswith('Snail Bed'))

    def test_snail_bed_snail_amount_default(self):
        snail_bed = SnailBedFactory(snail_amount=None)
        self.assertEqual(snail_bed.snail_amount, 0)

class SnailHatchRateTestCase(TestCase):
    def test_has_snail_bed(self):
        snail_hatch_rate = SnailHatchRateFactory()
        self.assertIsInstance(snail_hatch_rate.snail_bed, SnailBed)

    
    def test_snail_hatch_rate_creation(self):
        snail_hatch_rate = SnailHatchRateFactory()
        self.assertIsInstance(snail_hatch_rate, SnailHatchRate)

    def test_has_valid_datetime(self):
        snail_hatch_rate = SnailHatchRateFactory()
        self.assertIsInstance(snail_hatch_rate.datetime, datetime)

    def test_has_integer_preexisting_snail_amount(self):
        snail_hatch_rate = SnailHatchRateFactory()
        self.assertIsInstance(snail_hatch_rate.preexisting_snail_amount, int)

    def test_has_integer_newly_hatched_snails(self):
        snail_hatch_rate = SnailHatchRateFactory()
        self.assertIsInstance(snail_hatch_rate.newly_hatched_snails, int)

    def test_hatch_rate_percentage(self):
        snail_bed = snail_bed = SnailBedFactory(snail_amount=1000)
        snail_hatch_rate = SnailHatchRateFactory(
            snail_bed=snail_bed,
            preexisting_snail_amount = 1000,
            newly_hatched_snails = 400,
        )
        self.assertEqual(snail_hatch_rate.hatch_rate_percentage, 40)

class SnailMortalityRateTestCase(TestCase):
    def test_snail_mortality_rate_creation(self):
        snail_mortality_rate = SnailMortalityRateFactory()
        self.assertIsInstance(snail_mortality_rate, SnailMortalityRate)

    def test_has_snail_bed(self):
        snail_mortality_rate = SnailMortalityRateFactory()
        self.assertIsInstance(snail_mortality_rate.snail_bed, SnailBed)

    def test_has_valid_datetime(self):
        snail_mortality_rate = SnailMortalityRateFactory()
        self.assertIsInstance(snail_mortality_rate.datetime, datetime)

    def test_has_integer_preexisting_snail_amount(self):
        snail_mortality_rate = SnailMortalityRateFactory()
        self.assertIsInstance(snail_mortality_rate.preexisting_snail_amount, int)

    def test_has_integer_expired_snail_amount(self):
        snail_mortality_rate = SnailMortalityRateFactory()
        self.assertIsInstance(snail_mortality_rate.expired_snail_amount, int)

    def test_mortality_rate_percentage(self):
        snail_bed = snail_bed = SnailBedFactory(snail_amount=1000)
        snail_mortality_rate = SnailMortalityRateFactory(
            snail_bed=snail_bed,
            preexisting_snail_amount = 1000,
            expired_snail_amount = 300,
        )
        self.assertEqual(snail_mortality_rate.mortality_rate_percentage, 30)

class SnailFeedTestCase(TestCase):
    def test_snail_feed_creation(self):
        snail_feed = SnailFeedFactory()
        self.assertIsInstance(snail_feed, SnailFeed)

    def test_has_snail_bed(self):
        snail_feed = SnailFeedFactory()
        self.assertIsInstance(snail_feed.snail_bed, SnailBed)

    def test_has_valid_consumed_on_datetime(self):
        snail_feed = SnailFeedFactory()
        self.assertIsInstance(snail_feed.consumed_on, datetime)

    def test_has_integer_grams_feed_given(self):
        snail_feed = SnailFeedFactory()
        self.assertIsInstance(snail_feed.grams_feed_given, int)

class TimeTakenToMatureTestCase(TestCase):
    def test_has_snail_bed(self):
        time_taken_to_mature = TimeTakenToMatureFactory()
        self.assertIsInstance(time_taken_to_mature.snail_bed, SnailBed)

    def test_time_taken_to_mature_creation(self):
        time_taken_to_mature = TimeTakenToMatureFactory()
        self.assertIsInstance(time_taken_to_mature, TimeTakenToMature)

    def test_has_valid_hatched_datetime(self):
        time_taken_to_mature = TimeTakenToMatureFactory()
        self.assertIsInstance(time_taken_to_mature.snail_hatched, datetime)

    def test_has_valid_matured_datetime(self):
        time_taken_to_mature = TimeTakenToMatureFactory()
        self.assertIsInstance(time_taken_to_mature.snail_matured, datetime)

    def test_time_taken_to_mature_is_integer(self):
        # Convert date strings to datetime objects
        snail_hatched_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
        snail_matured_date = datetime.strptime("2023-01-05", "%Y-%m-%d")

        time_taken_to_mature = TimeTakenToMatureFactory(
            snail_hatched=snail_hatched_date,
            snail_matured=snail_matured_date,
        )
        self.assertIsInstance(time_taken_to_mature.days_to_mature, int)


    def test_time_taken_to_mature_days_to_mature(self):
        # Convert date strings to datetime objects
        snail_hatched_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
        snail_matured_date = datetime.strptime("2023-01-05", "%Y-%m-%d")

        time_taken_to_mature = TimeTakenToMatureFactory(
            snail_hatched=snail_hatched_date,
            snail_matured=snail_matured_date,
        )
        self.assertEqual(time_taken_to_mature.days_to_mature, 4)

    def test_period_is_timedelta(self):
        # Convert date strings to datetime objects
        snail_hatched_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
        snail_matured_date = datetime.strptime("2023-01-05", "%Y-%m-%d")

        time_taken_to_mature = TimeTakenToMatureFactory(
            snail_hatched=snail_hatched_date,
            snail_matured=snail_matured_date,
        )
        self.assertIsInstance(time_taken_to_mature.period, timedelta)

    def test_has_integer_snails_matured_count(self):
        time_taken_to_mature = TimeTakenToMatureFactory()
        self.assertIsInstance(time_taken_to_mature.snails_matured_count, int)