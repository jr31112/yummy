from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from api.pagination import PaginationHandlerMixin

from api import models, serializers
from django.db.models import Count

from django.db.models import Q
from api.MF import set_algo


class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

"""
Store API
 class Store            [stores/] [get, post]
 class StoreDetail      [stores/<int:pk>] [get, patch, delete]
"""
# stores/

class Store(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.StoreSerializer

# 가게 리스트를 불러오는 API
# query parameter [name, area]
# name=1987&area=세종
    def get(self, request, format=None, *args, **kwargs):
        # name -> store_name 에 검색
        # area -> address 에 검색
        # category -> category 검색

        name = request.query_params.get("name", None)
        area = request.query_params.get("area", None)
        category = request.query_params.get("category", None)
        order_by = request.query_params.get("order_by", None)

        # 기본 전체 store objects
        instance = models.Store.objects.all()

        if name is not None:
            instance = instance.filter(store_name__contains=name)
        if area is not None:
            instance = instance.filter(address__contains=area)
        if category is not None:
            instance = instance.filter(category__contains=category)

        # 커스텀 필드는 소트가 않데...
        if order_by is not None:
            desc = request.query_params.get("desc", None)
            # 이름 정렬
            if order_by =="name":
                if desc=='True' or desc is None:
                    instance = instance.order_by("store_name")
                elif desc=='False':
                    instance = instance.order_by("-store_name")

            # 리뷰 수에 따른 정렬
            elif order_by=="review":
                gte = request.query_params.get("gte", None)
                if gte is not None:
                    if desc =='True' or desc is None:
                        instance = instance.filter(review_count__gte=gte).order_by("review_count")
                    else:
                        instance = instance.filter(review_count__gte=gte).order_by("-review_count")
                else:
                    if desc=='True' or desc is None:
                        instance = instance.order_by("review_count")
                    else:
                        instance = instance.order_by("-review_count")


            # 평균 점수에 따른 정렬
            elif order_by =="score":
                if desc =='True' or desc is None:
                    instance = instance.extra(select={'avg':'review_total_score / review_count'}, order_by=('avg',))
                elif desc=='False':
                    instance = instance.extra(select={'avg':'review_total_score / review_count'}, order_by=('-avg',))

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.StoreListSerializer(page,
 many=True).data)
        else:
            serializer = serializers.StoreListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# 가게를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# stores/<int:pk>
class StoreDetail(APIView):
    serializer_class = serializers.StoreSerializer

    def get_object(self, id):
            store = get_object_or_404(models.Store, pk=id)
            return store
# 가게 id로 불러오는 API
    def get(self, request, pk):
        store = self.get_object(pk)
        serializer = self.serializer_class(store)
        # 해당 가게의 메뉴, 리뷰를 받아옴
        review = store.review_store.all()
        # print(store_detail.get('store_name'))
        sum=0
        for i in serializers.StoreReviewSerializer(review,many=True).data:
            sum+=i.get("total_score")
        # store 조회할때
        # id, detail(store정보), reviews, avg(평균 평점)
        avg = None if len(review)==0 else sum/len(review)
        result = {
        "id": pk,
        "detail":serializer.data,
        "review":serializers.StoreReviewSerializer(review, many=True).data,
        "avg_score" : avg
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        store = get_object_or_404(models.Store, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=store, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        store = get_object_or_404(models.Store, pk=pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def StoreRecommendations(request,pk):
    area = request.query_params.get("area", None)
    pred_result = set_algo(pk,area)
    # print(pred_result)
    result = []
    # 예상평점 없어 ~!
    for store_id in pred_result:
        result.append(serializers.StoreSerializer(models.Store.objects.get(pk=store_id)).data)

    return Response(result, status=status.HTTP_200_OK)

"""
Review API
class StoreReview            [stores/reivews/] [post]
class StoreReviewDetail      [stores/reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class StoreReview(APIView, PaginationHandlerMixin):
    serializer_class = serializers.StoreReviewSerializer

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            review_store = serializer.validated_data['store']
            store_update_data = {
            "review_count" : review_store.review_count+1,
            "review_total_score" : review_store.review_total_score + serializer.validated_data['total_score']
            }
            store_update = serializers.StoreListSerializer(data=store_update_data,instance=review_store,partial=True)
            if store_update.is_valid():
                store_update.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # stores/reviews/<int:pk>
class StoreReviewDetail(APIView):
    serializer_class = serializers.StoreReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.StoreReview, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.StoreReview, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)

        if serializer.is_valid():
            if 'total_score' in serializer.validated_data : # 평점을 변경하고 싶을 경우

                store_id = self.serializer_class(review).data['store']
                review_store = models.Store.objects.get(pk=store_id)
                review_store_serializer = serializers.StoreListSerializer(review_store)
                store_update_data = {
                "review_total_score" : review_store_serializer.data['review_total_score'] - review.total_score + serializer.validated_data['total_score']
                }
                store_update = serializers.StoreListSerializer(data=store_update_data, instance=review_store,partial=True)
                if store_update.is_valid():
                    store_update.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
                
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.StoreReview, pk=pk)
        store_id = self.serializer_class(review).data['store']
        review_store = models.Store.objects.get(pk=store_id)
        review_store_serializer = serializers.StoreListSerializer(review_store)

        store_update_data = {
        "review_count" : review_store_serializer.data['review_count']-1,
        "review_total_score" : review_store_serializer.data['review_total_score'] - review.total_score
        }

        store_update = serializers.StoreListSerializer(data=store_update_data,instance=review_store,partial=True)
        if store_update.is_valid():
            store_update.save()
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# 유저  id에 따른 작성 리뷰 리스트
class StoreReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.StoreReviewSerializer

    def get(self, request, pk):
        instance = models.StoreReview.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_user(request):
    error = UserSerializer.validate(get_user_model(), data=request.data)
    if error['password'] or error['email']:
        return Response(error, status=400)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = UserSerializer.create(get_user_model(), request.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }



"""
Spot API
 class Spot            [spots/] [get, post]
 class SpotDetail      [spots/<int:pk>] [get, patch, delete]
"""
class Spot(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.SpotSerializer

# 관광지 리스트를 불러오는 API
# query parameter [name, area]
    def get(self, request, format=None, *args, **kwargs):

        name = request.query_params.get("name", None)
        area = request.query_params.get("area", None)

        # 기본 전체 spot objects
        instance = models.Spot.objects.all()
        if name is not None:
            instance = instance.filter(spot_name__contains=name)
        if area is not None:
            instance = instance.filter(Q(road_address__contains=area) | Q(address__contains=area))

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.SpotListSerializer(page,
 many=True).data)
        else:
            serializer = self.serializers.SpotListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# 관광지를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# spots/<int:pk>
class SpotDetail(APIView):
    serializer_class = serializers.SpotSerializer

    def get_object(self, id):
            spot = get_object_or_404(models.Spot, pk=id)
            return spot
# 관광지 id로 불러오는 API
    def get(self, request, pk):
        spot = self.get_object(pk)
        serializer = self.serializer_class(spot)
        review = spot.spotreview_spot.all()
        result = {
            "detail" : serializer.data,
            "review" : serializers.SpotReviewSerializer(review, many=True).data
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        spot = get_object_or_404(models.Spot, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=spot, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        spot = get_object_or_404(models.Spot, pk=pk)
        spot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



"""
 Spot Review API
class SpotReview            [spots/reivews/] [post]
class SpotReviewDetail      [spots/reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class SpotReview(APIView, PaginationHandlerMixin):
    serializer_class = serializers.SpotReviewSerializer

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # stores/reviews/<int:pk>
class SpotReviewDetail(APIView):
    serializer_class = serializers.SpotReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.SpotReview, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.SpotReview, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.SpotReview, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 유저  id에 따른 작성 리뷰 리스트
class SpotReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.SpotReviewSerializer

    def get(self, request, pk):
        instance = models.SpotReview.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


"""
Lodging API
 class Lodging            [lodgings/] [get, post]
 class LodgingDetail      [lodgings/<int:pk>] [get, patch, delete]
"""
class Lodging(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.LodgingSerializer

# 관광지 리스트를 불러오는 API
# query parameter [name, area]
    def get(self, request, format=None, *args, **kwargs):

        name = request.query_params.get("name", None)
        area = request.query_params.get("area", None)

        # 기본 전체 spot objects
        instance = models.Lodging.objects.all()
        if name is not None:
            instance = instance.filter(lodging_name__contains=name)
        if area is not None:
            instance = instance.filter(Q(road_address__contains=area) | Q(address__contains=area))

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(serializers.LodgingListSerializer(page,
 many=True).data)
        else:
            serializer = serializers.LodgingListSerializer(instance, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# 숙박시설를 추가하는 API
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# lodgings/<int:pk>
class LodgingDetail(APIView):
    serializer_class = serializers.LodgingSerializer

    def get_object(self, id):
            lodging = get_object_or_404(models.Lodging, pk=id)
            return lodging
# 숙박업소 id로 불러오는 API
    def get(self, request, pk):
        lodging = self.get_object(pk)
        serializer = self.serializer_class(lodging)
        review = lodging.lodgingreview_lodging.all()
        result = {
            "detail" : serializer.data,
            "review" : serializers.LodgingReviewSerializer(review, many=True).data
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        lodging = get_object_or_404(models.Lodging, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=lodging, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        lodging = get_object_or_404(models.Lodging, pk=pk)
        lodging.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



"""
Lodging Review API
class LodgingReview            [lodgings/reivews/] [post]
class LodgingReviewDetail      [lodgings/reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class LodgingReview(APIView, PaginationHandlerMixin):
    serializer_class = serializers.LodgingReviewSerializer

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    # lodgings/reviews/<int:pk>
class LodgingReviewDetail(APIView):
    serializer_class = serializers.SpotReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.LodgingReview, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.LodgingReview, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.LodgingReview, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def create_user(request):
    error = UserSerializer.validate(get_user_model(), data=request.data)
    if error['password'] or error['email']:
        return Response(error, status=400)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = UserSerializer.create(get_user_model(), request.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
# 유저  id에 따른 작성 리뷰 리스트
class LodgingReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.LodgingReviewSerializer

    def get(self, request, pk):
        instance = models.LodgingReview.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def ReviewByUser(request,pk):
    store_reviews = models.StoreReview.objects.filter(user=pk)
    spot_reviews = models.SpotReview.objects.filter(user=pk)
    lodging_reviews = models.LodgingReview.objects.filter(user=pk)
    result = {
        "store" : serializers.StoreReviewSerializer(store_reviews, many=True).data,
        "spot" : serializers.SpotReviewSerializer(spot_reviews, many=True).data,
        "lodging" : serializers.LodgingReviewSerializer(lodging_reviews, many=True).data
    }
    return Response(result, status=status.HTTP_200_OK)
