from django.contrib import admin

from .models import SnailFeed, SnailHatchRate, SnailMortalityRate, TimeTakenToMature, SnailBedPerformance, ForecastedHatchRate, SnailBed
from .models import AdminUser, EmployeeUser


admin.site.register(SnailFeed)
admin.site.register(SnailHatchRate)
admin.site.register(SnailMortalityRate)
admin.site.register(TimeTakenToMature)
admin.site.register(SnailBedPerformance)
admin.site.register(ForecastedHatchRate)
admin.site.register(SnailBed)

admin.site.register(AdminUser)
admin.site.register(EmployeeUser)


from django.contrib.auth.admin import UserAdmin
from .models import EmployeeUser

class EmployeeUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
