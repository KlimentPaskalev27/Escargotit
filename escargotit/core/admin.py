from django.contrib import admin
from .models import Admin, User, SnailBed, SnailFeed, Medicine, StaffUsableItems, InventoryPanel, SnailPerformance, Feed, CleaningProducts

admin.site.register(Admin)

admin.site.register(User)

admin.site.register(SnailBed)

admin.site.register(SnailFeed)

admin.site.register(Medicine)

admin.site.register(StaffUsableItems)

admin.site.register(InventoryPanel)
admin.site.register(SnailPerformance)
admin.site.register(Feed)
admin.site.register(CleaningProducts)