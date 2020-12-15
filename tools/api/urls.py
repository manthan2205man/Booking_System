from django.urls import path
from tools.api import views
# app_name = 'tools_api'

urlpatterns = [
    path('create_tool', views.ToolCreatView.as_view(), name='create_tool'),
    path('create_booking', views.BookingCreatView.as_view(), name='create_booking'),
    path('delete_booking/<str:pk>/', views.BookingDeleteView.as_view(), name='delete_booking'),
    path('update_tool/<str:pk>/', views.ToolUpdateView.as_view(), name='update_tool'),
    path('list_tool/', views.ToolListView.as_view(), name='list_tool'),
    path('filter_tool/', views.ToolFilterView.as_view(), name='filter_tool'),
]
