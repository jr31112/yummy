from django.utils import timezone
from django.db import models
import secrets
import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


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
    review_count = models.IntegerField(blank=True, null=True)
    review_total_score = models.IntegerField(blank=True, null=True)

    @property
    def category_list(self):
        return self.category.split("|") if self.category else []

# 2 User
class User(AbstractBaseUser):
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
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name = "review_id")
    total_score = models.FloatField(max_length=50, blank=False)
    content = models.TextField()
    reg_time = models.DateTimeField(auto_now_add=True)


# 4 Spot(관광지)
class Spot(models.Model):
    id = models.IntegerField(primary_key=True) #auto increment
    spot_name = models.CharField(max_length=50)
    road_address  = models.CharField(max_length=200, null=True,  blank=True)
    address= models.CharField(max_length=200, null=True,  blank=True)
    latitude = models.FloatField(max_length=10, null=True,  blank=True)
    longitude = models.FloatField(max_length=10, null=True,  blank=True)
    description = models.TextField()


# 5 Lodging (숙박업소)
class Lodging(models.Model):
    id = models.IntegerField(primary_key=True) #auto increment
    lodging_name = models.CharField(max_length=50)
    lodging_type = models.CharField(max_length=50)
    road_address = models.CharField(max_length=200, null=True,  blank=True)
    address= models.CharField(max_length=200, null=True,  blank=True)
    latitude = models.FloatField(max_length=10, null=True,  blank=True)
    longitude = models.FloatField(max_length=10, null=True,  blank=True)
    description = models.TextField()

# 4-1 관광지 Review
class SpotReview(models.Model):
    id = models.AutoField(primary_key=True) #auto increment
    spot = models.ForeignKey(Spot, null=False, blank=False, on_delete=models.CASCADE, related_name="review_spot")
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name = "spotreview_id")
    total_score = models.FloatField(max_length=50, blank=False)
    content = models.TextField()
    reg_time = models.DateTimeField(auto_now_add=True)

# 5-1 숙박업소 Review
class LodgingReview(models.Model):
    id = models.AutoField(primary_key=True) #auto increment
    lodging = models.ForeignKey(Lodging, null=False, blank=False, on_delete=models.CASCADE, related_name="review_lodging")
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name = "lodgingreview_id")
    total_score = models.FloatField(max_length=50, blank=False)
    content = models.TextField()
    reg_time = models.DateTimeField(auto_now_add=True)

# //TODO : 일정 저장 Model 짜야해
