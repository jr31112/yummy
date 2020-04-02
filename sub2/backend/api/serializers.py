from .models import Store, User
from django.contrib.auth import get_user_model
from .models import Store, CustomUser, Review, Menu
from rest_framework import serializers

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['gender', 'birth_year', 'email', 'nickname']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email = validated_data["email"],
            gender = validated_data["gender"],
            birth_year = validated_data["birth_year"],
            nickname = validated_data["nickname"],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        model = CustomUser
        fields = [
            "id",
            "gender",
            "birth_year",
            "email",
            "nickname",
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "store",
            "user",
            "total_score",
            "content",
            "reg_time",
        ]

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "store",
            "menu_name",
            "price",
        ]
