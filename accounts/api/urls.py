from django.urls import path
from accounts.api import views

# app_name = 'accounts_api'

urlpatterns = [
    path('test/', views.test.as_view(), name='test'),
    path('user_create/', views.UserCreatView.as_view(), name='owner_create'),
    path('user_login/', views.LoginView.as_view(), name='user_login'),
]