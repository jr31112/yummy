from .models import Store, User, Spot, Lodging, SpotReview, LodgingReview ,StoreReview, Plan, PlanDay, Itinerary
from rest_framework import serializers
from django.contrib.auth import get_user_model

# Store
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
        "address",
        "latitude",
        "longitude",
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
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    gender = serializers.CharField()
    birth_year = serializers.IntegerField()
    nickname = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "gender", "password1", "password2", "birth_year", "nickname"]
        

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data["email"],
            gender = validated_data["gender"],
            birth_year = validated_data["birth_year"],
            nickname = validated_data["nickname"]
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
       password1 = validated_data.pop("password1")
       instance.__dict__.update(validated_data)
       if password1:
           instance.set_password(password)
       instance.save()
       return instance
       
    def validate(self, data):
        non_alpha = set([s for s in "!@#$%^&*()|-=_+\[]{};':\",./?><"])
        error = dict({'email' : [], 'password': []})
        if data['password1'] != data['password2']: # confirm error: 1
            error['password'].append('비밀번호 같게 해주세요')
        if not 8 <= len(data['password1']) < 16:   # password length error: 2
            error['password1'].append('비밀번호를 8 ~ 16자로 작성해주세요!')
        if data['password1'].isdigit():  # password is only numbers: 3
            error['password'].append('비밀번호를 다른 문자와 조합해주세요!')
        if get_user_model().objects.filter(email= data['email']): # same username in db : 4
            error['email'].append('중복된 ID가 있습니다.')
        # if non_alpha not in data['password1']: # non_alph in username: 6
        #     error['password'].append('비밀번호에 특수문자를 넣어주세요!')
        return error

# store review
class StoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = [
            "id",
            "store",
            "user",
            "total_score",
            "content",
            "reg_time",
        ]

# 장소
# 장소 리스트
class SpotListSerializer(serializers.ModelSerializer):
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Spot
        fields = [
            "id",
            "spot_name",
            "road_address",
            "address",
            "latitude",
            "longitude",
            "review_avg_score",
        ]
    def get_review_avg_score(self, obj):
        if(obj.spotreview_spot.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.spotreview_spot.all():
                sum+=rev.total_score
            return sum/obj.spotreview_spot.count()

 # 장소
class SpotSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(
    source='spotreview_spot.count'
)
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Spot
        fields = [
            "id",
            "spot_name",
            "road_address",
            "address",
            "latitude",
            "longitude",
            "description",
            "review_avg_score",
            "review_count"
        ]
    def get_review_avg_score(self, obj):
        if(obj.spotreview_spot.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.spotreview_spot.all():
                sum+=rev.total_score
            return sum/obj.spotreview_spot.count()

# 숙박 리스트
class LodgingListSerializer(serializers.ModelSerializer):
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Lodging
        fields = [
            "id",
            "lodging_name",
            "lodging_type",
            "road_address",
            "address",
            "latitude",
            "longitude",
            "review_avg_score",
        ]
    def get_review_avg_score(self, obj):
        if(obj.lodgingreview_lodging.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.lodgingreview_lodging.all():
                sum+=rev.total_score
            return sum/obj.lodgingreview_lodging.count()

# 숙박
class LodgingSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(
    source='lodgingreview_lodging.count'
)
    review_avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Lodging
        fields = [
            "id",
            "lodging_name",
            "lodging_type",
            "road_address",
            "address",
            "latitude",
            "longitude",
            "description",
            "review_avg_score",
            "review_count"
        ]
    def get_review_avg_score(self, obj):
        if(obj.lodgingreview_lodging.count()==0):
            return 0
        else:
            sum = 0
            for rev in obj.lodgingreview_lodging.all():
                sum+=rev.total_score
            return sum/obj.lodgingreview_lodging.count()

# 장소 리뷰
class SpotReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotReview
        fields = [
            "id",
            "spot",
            "user",
            "total_score",
            "content",
            "reg_time",
        ]

# 숙박 리뷰
class LodgingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgingReview
        fields = [
            "id",
            "lodging",
            "user",
            "total_score",
            "content",
            "reg_time",
        ]

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "user_id",
            "title",
            "content",
            "start_date",
            "end_date"
        ]

class PlanDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDay
        fields = [
            "id",
            "plan_id",
            "date",
        ]

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = [
            "id",
            "day_id",
            "start_time",
            "end_time",
            "store",
            "spot",
            "lodging"
        ]