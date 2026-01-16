from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class TaxZone(models.Model):
    zone_code = models.AutoField(primary_key=True)
    zone_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.zone_name


class TaxCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    tax_type = models.CharField(max_length=30)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.tax_type


# Auth Models

class CustomUser(AbstractUser):
    username = None
    user_id = models.BigAutoField(primary_key=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.user_id


# Profile Models

class TaxPayerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tin = models.BigAutoField(primary_key=True)

    tax_zone = models.ForeignKey(TaxZone, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10)

    # Address and Contact Information
    house = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    phone1 = models.CharField(max_length=15, blank=True)
    phone2 = models.CharField(max_length=15, blank=True)
    phone3 = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.tin} - {self.first_name}"
