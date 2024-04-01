
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('student/',StudentList.as_view()),
    path('student/<int:pk>',StudentDetail.as_view()),

    path('academicprogram/',AcademicProgramList.as_view()),
    path('academicprogram/<int:pk>',AcademicProgramDetail.as_view()),
]   
