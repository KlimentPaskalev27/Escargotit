from django import forms
from .models import SnailFeed, Medicine, StaffUsableItems, InventoryPanel

class SnailFeedForm(forms.ModelForm):
    class Meta:
        model = SnailFeed
        fields = ['name', 'category', 'stock_amount']


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'stock_amount']


class StaffUsableItemsForm(forms.ModelForm):
    class Meta:
        model = StaffUsableItems
        fields = ['name', 'category', 'stock_amount']


class InventoryPanelForm(forms.ModelForm):
    class Meta:
        model = InventoryPanel
        fields = ['snail_feed', 'medicine', 'staff_usable_items']
