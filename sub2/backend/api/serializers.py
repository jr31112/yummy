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

class StoreListSerializer(serializers.ModelSerializer):
#     review_store = serializers.StringRelatedField(many=True)
#     review_count = serializers.IntegerField(
#     source='review_store.count'
# )
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = [
        "id",
        "store_name",
        "branch",
        "area",
        "category_list",
        "review_count",
        "review_total_score",
        "review_avg_score"
        ]
    def get_review_avg_score(self, obj):
        if(obj.review_count==0):
            return 0
        else:
            return obj.review_total_score/obj.review_count

class UserSerializer(serializers.ModelSerializer):
    class Meta:
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
