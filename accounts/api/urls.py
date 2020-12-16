from django.urls import path
from accounts.api import views

# app_name = 'accounts_api'

urlpatterns = [
    path('test/', views.test.as_view()),
    path('user_create/', views.UserCreatView.as_view()),
    path('user_login/', views.LoginView.as_view()),
]