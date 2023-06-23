from django.core.management.base import BaseCommand
from core.models import SnailFeed, SnailBirthRate, SnailMortalityRate, TimeTakenToMature

class Command(BaseCommand):
    help = 'Populates dummy records for each class'

    def handle(self, *args, **options):
        # Populate dummy records for SnailFeed
        snail_feed = SnailFeed(consumed_on='2023-06-23', grams_feed_given=100)
        snail_feed.save()

        # Populate dummy records for SnailBirthRate
        snail_birth_rate = SnailBirthRate(preexisting_snail_amount=50, newly_hatched_snails=20)
        snail_birth_rate.save()

        # Populate dummy records for SnailMortalityRate
        snail_mortality_rate = SnailMortalityRate(preexisting_snail_amount=100, expired_snail_amount=10)
        snail_mortality_rate.save()

        # Populate dummy records for TimeTakenToMature
        time_taken_to_mature = TimeTakenToMature(snail_hatched='2023-01-01', snail_matured='2023-06-01')
        time_taken_to_mature.save()

        self.stdout.write(self.style.SUCCESS('Dummy records populated successfully.'))
