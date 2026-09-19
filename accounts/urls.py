from django.urls import path

from . import views

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenBlacklistView,TokenRefreshView)

urlpatterns = [
    path('',views.home,name='home'),
    path('api/auth/register/',views.Register.as_view(),name='register'),
    path('api/auth/login/',TokenObtainPairView.as_view(),name='login'),
    path('api/auth/token/refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('api/auth/logout/',TokenBlacklistView.as_view(),name='logout'),
    path('api/auth/me/',views.Me.as_view(),name='me'),
]