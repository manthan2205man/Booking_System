from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    # path('customer_register/', views.customer_register, name='customer_register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]