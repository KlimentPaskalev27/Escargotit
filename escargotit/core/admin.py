from django.contrib import admin

from .models import SnailFeed, SnailHatchRate, SnailMortalityRate, TimeTakenToMature, SnailBedPerformance, ForecastedHatchRate, SnailBed,Profile

admin.site.register(SnailFeed)
admin.site.register(SnailHatchRate)
admin.site.register(SnailMortalityRate)
admin.site.register(TimeTakenToMature)
admin.site.register(SnailBedPerformance)
admin.site.register(ForecastedHatchRate)
admin.site.register(SnailBed)

admin.site.register(Profile)