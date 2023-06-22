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