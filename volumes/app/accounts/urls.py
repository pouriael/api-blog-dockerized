
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.authtoken import views as auth_token
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
        path('register/',views.UserRegistrationView.as_view()),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('login/', views.UserLoginView.as_view(),name='login'),
        path('profile/', views.UserProfileView.as_view(),name='profile'),
        path('changepassword/', views.UserChangePasswordView.as_view(),name='changepassword'),
        path('send=reset-password-email/', views.SendPasswordResetEmailView.as_view(),name='send=reset-password-email'),
        path('reset-password/<uid>/<token>/', views. UserPasswordResetView.as_view(),name='reset-password'),
  
    ]

router = routers.SimpleRouter()
router.register('user',views.UserViewSet)
urlpatterns += router.urls