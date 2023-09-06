from django.contrib import admin

from .models import SnailFeed, SnailHatchRate, SnailMortalityRate, TimeTakenToMature, SnailPerformance, ForecastedHatchRate, SnailBed

admin.site.register(SnailFeed)
admin.site.register(SnailHatchRate)
admin.site.register(SnailMortalityRate)
admin.site.register(TimeTakenToMature)
admin.site.register(SnailPerformance)
admin.site.register(ForecastedHatchRate)
admin.site.register(SnailBed)