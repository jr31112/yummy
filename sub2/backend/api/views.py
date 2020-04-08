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

        # //  TODO:  Req 2-1 종류, 리뷰 수 등 다양한 검색조건 추가 & 정렬
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
                if desc =='True' or desc is None:
                    instance = instance.filter(review_count__gte=gte).order_by("review_count")
                elif desc=='False':
                    instance = instance.filter(review_count__gte=gte).order_by("-review_count")

            # 평균 점수에 따른 정렬
            elif order_by =="score":
                gte = request.query_params.get("gte", None)
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
        menu = store.menu_store.all()
        review = store.review_store.all()
        # print(store_detail.get('store_name'))
        sum=0
        for i in serializers.ReviewSerializer(review,many=True).data:
            sum+=i.get("total_score")
        # store 조회할때
        # id, detail(store정보), menus, reviews, avg(평균 평점)
        avg = None if len(review)==0 else sum/len(review)
        result = {
        "id": pk,
        "detail":serializer.data,
        "menu": serializers.MenuSerializer(menu,many=True).data,
        "review":serializers.ReviewSerializer(review, many=True).data,
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


"""
Review API
class Review            [reivews/] [get, post]
class ReviewDetail      [reviews/<int:pk>] [get, patch, delete]
"""
# reviews/
class Review(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.ReviewSerializer

    # 리뷰 리스트를 불러오는 API
    def get(self, request, format=None, *args, **kwargs):
        instance = models.Review.objects.all()

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 리뷰를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # reviews/<int:pk>
class ReviewDetail(APIView):
    serializer_class = serializers.ReviewSerializer

    def get_object(self, id):
            review = get_object_or_404(models.Review, pk=id)
            return review
    # 리뷰 id로 불러오는 API
    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = self.serializer_class(review)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = get_object_or_404(models.Review, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=review, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        review = get_object_or_404(models.Review, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 유저  id에 따른 작성 리뷰 리스트
class ReviewByUser(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.ReviewSerializer

    def get(self, request, pk):
        instance = models.Review.objects.all().filter(user=pk)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else :
            serializer = self.serializer_class(instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

"""
Menu API
class Menu            [menus/] [get, post]
class MenuDetail      [menus/<int:pk>] [get, patch, delete]
"""
# menus/
class Menu(APIView, PaginationHandlerMixin):
    pagination_class = SmallPagination
    serializer_class = serializers.MenuSerializer

    # 메뉴 리스트를 불러오는 API
    def get(self, request, format=None, *args, **kwargs):
        instance = models.Menu.objects.all()

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
    many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 메뉴를 추가하는 API
    def post(self, request, format=None):
    # request.POST : FormData로 POST 전송이 되었을 때
    # request.data : FormData로 POST 전송 및 data로 되었을 때
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # menus/<int:pk>
class MenuDetail(APIView):
    serializer_class = serializers.MenuSerializer

    def get_object(self, id):
            menu = get_object_or_404(models.Menu, pk=id)
            return menu
    # 메뉴 id로 불러오는 API
    def get(self, request, pk):
        menu = self.get_object(pk)
        serializer = self.serializer_class(menu)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        menu = get_object_or_404(models.Menu, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=menu, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


    # 삭제
    def delete(self, request, pk, format=None):
        menu = get_object_or_404(models.Menu, pk=pk)
        menu.delete()
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
