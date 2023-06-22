from django.db import models
from django.contrib.auth.models import AbstractUser

class Admin(models.Model):
    # Additional fields for the admin model
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.full_name


class User(AbstractUser):
    # Inherits fields from the AbstractUser model
    # (e.g., username, password, email, first_name, last_name, etc.)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
class SnailBed(models.Model):
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    productivity = models.DecimalField(max_digits=5, decimal_places=2)
    mortality_rate = models.DecimalField(max_digits=5, decimal_places=2)
    feed_level = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Snail Bed #{self.id}"
    

class SnailFeed(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock_amount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock_amount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class StaffUsableItems(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    stock_amount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class InventoryPanel(models.Model):
    snail_feed = models.ForeignKey(SnailFeed, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    staff_usable_items = models.ForeignKey(StaffUsableItems, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Inventory Panel #{self.id}"
    

class SnailPerformance(models.Model):
    birth_rate = models.DecimalField(max_digits=5, decimal_places=2)
    mortality_rate = models.DecimalField(max_digits=5, decimal_places=2)
    feed_consumption = models.DecimalField(max_digits=10, decimal_places=2)
    time_to_maturity = models.DecimalField(max_digits=5, decimal_places=2)
    snail_bed = models.ForeignKey(SnailBed, on_delete=models.CASCADE)

    @property
    def snail_performance(self):
        return (self.birth_rate - self.mortality_rate) * self.feed_consumption / self.time_to_maturity

    def __str__(self):
        return f"Snail Performance for Snail Bed #{self.snail_bed.id}"
    


ANIMAL_FEED_INGREDIENTS = [
    ('Corn', 'Corn'),
    ('Soybean Meal', 'Soybean Meal'),
    ('Wheat', 'Wheat'),
    ('Barley', 'Barley'),
    ('Oats', 'Oats'),
    ('Fish Meal', 'Fish Meal'),
    ('Bone Meal', 'Bone Meal'),
    ('Canola Meal', 'Canola Meal'),
    ('Cottonseed Meal', 'Cottonseed Meal'),
    ('Peas', 'Peas'),
    ('Rice Bran', 'Rice Bran'),
    ('Alfalfa Meal', 'Alfalfa Meal'),
    ('Molasses', 'Molasses'),
    ('Dried Distillers Grains', 'Dried Distillers Grains'),
    ('Sunflower Meal', 'Sunflower Meal'),
]

class Feed(models.Model):
    ingredient = models.CharField(max_length=100, choices=ANIMAL_FEED_INGREDIENTS)
    # Add other fields as needed

    def __str__(self):
        return self.ingredient
    

STAFF_USABLE_ITEMS = [
    ('Shovel', 'Shovel'),
    ('Rake', 'Rake'),
    ('Wheelbarrow', 'Wheelbarrow'),
    ('Pruning Shears', 'Pruning Shears'),
    ('Gloves', 'Gloves'),
    ('Bucket', 'Bucket'),
    ('Hoe', 'Hoe'),
    ('Sprayer', 'Sprayer'),
    ('Secateurs', 'Secateurs'),
    ('Pitchfork', 'Pitchfork'),
]

class StaffUsableItems(models.Model):
    item = models.CharField(max_length=100, choices=STAFF_USABLE_ITEMS)
    # Add other fields as needed

    def __str__(self):
        return self.item
    


CLEANING_PRODUCTS = [
    ('Sanitizing Solution', 'Sanitizing Solution'),
    ('Degreaser', 'Degreaser'),
    ('All-Purpose Cleaner', 'All-Purpose Cleaner'),
    ('Disinfectant Spray', 'Disinfectant Spray'),
    ('Floor Cleaner', 'Floor Cleaner'),
    ('Glass Cleaner', 'Glass Cleaner'),
    ('Oven Cleaner', 'Oven Cleaner'),
    ('Drain Cleaner', 'Drain Cleaner'),
    ('Stainless Steel Polish', 'Stainless Steel Polish'),
    ('Dishwashing Liquid', 'Dishwashing Liquid'),
    ('Surface Disinfectant', 'Surface Disinfectant'),
    ('Air Freshener', 'Air Freshener'),
    ('Carpet Cleaner', 'Carpet Cleaner'),
    ('Tile and Grout Cleaner', 'Tile and Grout Cleaner'),
    ('Mold and Mildew Remover', 'Mold and Mildew Remover'),
    ('Hand Soap', 'Hand Soap'),
    ('Insecticide', 'Insecticide'),
    ('Floor Polish', 'Floor Polish'),
    ('Lubricant', 'Lubricant'),
    ('Rust Remover', 'Rust Remover'),
]


class CleaningProducts(models.Model):
    product = models.CharField(max_length=100, choices=CLEANING_PRODUCTS)
    # Add other fields as needed

    def __str__(self):
        return self.product