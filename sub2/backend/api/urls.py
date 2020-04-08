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

    path('reviews/', views.Review.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()),
    path('reviews/user/<int:pk>/', views.ReviewByUser.as_view()),


]
