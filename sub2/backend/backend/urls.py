from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from api.views import create_user

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path('login/', obtain_jwt_token),
    path('signup/', create_user)
]
# fmt: on
