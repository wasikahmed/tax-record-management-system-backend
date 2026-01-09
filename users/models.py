from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.user_id


class TaxOfficerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    officer_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    rank = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    house_no = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.IntegerField()



class TaxPayerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    tin = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    house = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.IntegerChoices()
    phone1 = models.CharField(max_length=50)
    phone2 = models.CharField(max_length=50, blank=True, null=True)
    phone3 = models.CharField(max_length=50, blank=True, null=True)
