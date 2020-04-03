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
        model = CustomUser
        fields = ["id", "email", "gender", "birth_year",  "nickname",]
        def create(self, validated_data):
            user = get_user_model().objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
            gender = validated_data['gender'],
            birth_year = validated_data['birth_year'],
            nickname = validated_data['nickname']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

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
