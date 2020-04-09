from rest_framework import permissions
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    #class -> as view
    # def -> x
    path('stores/', views.Store.as_view()),
    path('stores/<int:pk>/', views.StoreDetail.as_view()),
    # 메뉴 추천
    path('stores/recommendations/<int:pk>/', views.StoreRecommendations),

    path('stores/reviews/', views.StoreReview.as_view()),
    path('stores/reviews/<int:pk>/', views.StoreReviewDetail.as_view()),
    path('stores/reviews/user/<int:pk>/', views.StoreReviewByUser.as_view()),

    path('spots/', views.Spot.as_view()),
    path('spots/<int:pk>/', views.SpotDetail.as_view()),

    path('spots/reviews/', views.SpotReview.as_view()),
    path('spots/reviews/<int:pk>/', views.SpotReviewDetail.as_view()),
    path('spots/reviews/user/<int:pk>/', views.SpotReviewByUser.as_view()),
    
    path('lodgings/', views.Lodging.as_view()),
    path('lodgings/<int:pk>/', views.LodgingDetail.as_view()),

    path('lodgings/reviews/', views.LodgingReview.as_view()),
    path('lodgings/reviews/<int:pk>/', views.LodgingReviewDetail.as_view()),
    path('lodgings/reviews/user/<int:pk>/', views.LodgingReviewByUser.as_view()),

    # 유저아이디로 작성한 전체 리뷰 검색
    path('reviews/user/<int:pk>/', views.ReviewByUser),

]
