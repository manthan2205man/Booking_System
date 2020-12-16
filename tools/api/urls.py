from django.urls import path
from tools.api import views
# app_name = 'tools_api'

urlpatterns = [
    path('create_tool', views.ToolCreatView.as_view()),
    path('create_booking', views.BookingCreatView.as_view()),
    path('delete_booking/<str:pk>/', views.BookingDeleteView.as_view()),
    path('update_tool/<str:pk>/', views.ToolUpdateView.as_view()),
    path('list_tool/', views.ToolListView.as_view()),
    path('filter_tool/', views.ToolFilterView.as_view()),
    path('order/<int:pk>/', views.order),
    path('handlerequest/', views.handlerequest),
    path('rating/<int:id>/', views.rating),
]
