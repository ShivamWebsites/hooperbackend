from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registerview'),
    path('verify-email/<str:uid>/<str:token>/', views.VerifyEmail.as_view(), name='verify_email'),
    path('login/', views.LoginView.as_view(), name='loginview'),
    path('forget-password/', views.ForgetPassword.as_view(), name='forget-password'),
    path('reset-password/<str:token>/<str:uid>/', views.ResetPassword.as_view(), name='reset-password'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
]
urlpatterns += router.urls
