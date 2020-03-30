from django.utils import timezone
from django.db import models
import secrets
import datetime
from django.contrib.auth.models import AbstractUser

# 1 Store
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20, null=True, blank=True)
    area = models.CharField(max_length=50, null=True,  blank=True)
    tel = models.CharField(max_length=20, null=True,  blank=True)
    address = models.CharField(max_length=200, null=True,  blank=True)
    latitude = models.FloatField(max_length=10, null=True,  blank=True)
    longitude = models.FloatField(max_length=10, null=True,  blank=True)
    category = models.CharField(max_length=200,  null=True, blank=True)

    @property
    def category_list(self):
        return self.category.split("|") if self.category else []


# 2 User
class User(AbstractUser):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True) #auto increment
    gender = models.CharField(max_length=5, blank=False)
    birth_year = models.IntegerField(blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False, unique = True)
    nickname = models.CharField(max_length=20, blank=False)


# 3 Review
class Review(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True) #auto increment
    store = models.ForeignKey(Store, null=False, blank=False, on_delete=models.CASCADE, related_name="review_store")
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name = "review_id")
    total_score = models.FloatField(max_length=50, blank=False)
    content = models.TextField()
    reg_time = models.DateTimeField(auto_now_add=True)

# 4 Menu
class Menu(models.Model):
    id = models.IntegerField(primary_key=True) #auto increment
    store = models.ForeignKey(Store, null=False, blank=False, on_delete=models.CASCADE, related_name="menu_store")
    menu_name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField(default=0)
