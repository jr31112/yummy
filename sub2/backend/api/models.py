from django.utils import timezone
from django.db import models
import secrets
import datetime
from django.contrib.auth.models import AbstractBaseUser

# 1 Store
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20, blank=True)
    area = models.CharField(max_length=50, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(max_length=10, null=True, blank=True)
    longitude = models.FloatField(max_length=10, null=True, blank=True)
    category = models.CharField(max_length=200, blank=True)

    @property
    def category_list(self):
        return self.category.split("|") if self.category else []

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

# 2 User
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=5)
    birth_year = models.IntegerField()
    email = models.EmailField(max_length=50, unique = True)
    nickname = models.CharField(max_length=20)
    USERNAME

# 3 Review
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="review_store")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "review_id")
    total_score = models.FloatField(max_length=50)
    content = models.TextField()
    reg_time = models.DateTimeField(auto_now_add=True)

# 4 Menu
class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="menu_store")
    menu_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
