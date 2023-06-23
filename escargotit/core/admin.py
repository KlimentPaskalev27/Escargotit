from django.contrib import admin

from .models import SnailFeed, SnailBirthRate, SnailMortalityRate, TimeTakenToMature, SnailPerformance

admin.site.register(SnailFeed)
admin.site.register(SnailBirthRate)
admin.site.register(SnailMortalityRate)
admin.site.register(TimeTakenToMature)
admin.site.register(SnailPerformance)