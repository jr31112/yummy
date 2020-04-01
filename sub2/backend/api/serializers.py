from .models import Store, User
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
        model = User
        fields = ['gender', 'birth_year', 'email', 'nickname']

        def create(self, validated_data):
            user = get_user_model().objects.create(
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
