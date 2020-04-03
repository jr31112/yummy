from django.utils import timezone
from django.db import models
import secrets
import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

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

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.TextField(blank=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

# 2 User
class CustomUser(AbstractBaseUser):
    id =  models.AutoField(primary_key=True)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    birth_year = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True)
    nickname = models.CharField(max_length=20, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

# 3 Review
class Review(models.Model):
    # id = models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True) #auto increment
    store = models.ForeignKey(Store, null=False, blank=False, on_delete=models.CASCADE, related_name="review_store")
    user = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, related_name = "review_id")
    total_score = models.FloatField(max_length=50, blank=False)
    content = models.TextField()
    reg_time = models.DateTimeField(auto_now_add=True)

# 4 Menu
class Menu(models.Model):
    id = models.IntegerField(primary_key=True) #auto increment
    store = models.ForeignKey(Store, null=False, blank=False, on_delete=models.CASCADE, related_name="menu_store")
    menu_name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField(default=0)
