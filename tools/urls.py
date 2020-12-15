from django.urls import path,include
from . import views


urlpatterns = [
    path('my_tools/', views.my_tools, name='my_tools'),
    path('add_tools/', views.add_tools, name='add_tools'),
    path('edit_tools/<int:id>/', views.edit_tools, name='edit_tools'),
    path('delete_tools/<int:id>/', views.delete_tools, name='delete_tools'),
    path('add_multipleimages/<int:id>/', views.add_multipleimages, name='add_multipleimages'),
    path('save_tools/<int:id>/', views.save_tools, name='save_tools'),
    path('save_for_later/', views.save_for_later, name='save_for_later'),
    path('delete_save/<int:id>/', views.delete_save, name='delete_save'),

    path('tools_details/<int:id>/', views.tools_details, name='tools_details'),
    path('booknow/<int:id>/', views.booknow, name='booknow'),
    path('booknowdetails/<int:id>/', views.booknowdetails, name='booknowdetails'),
    path('order/<int:id>/', views.order, name='order'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
    path('show_my_booking/', views.show_my_booking, name='show_my_booking'),
    path('complete_payment/<int:id>', views.complete_payment, name='complete_payment'),
    path('show_payment/', views.show_payment, name='show_payment'),
    path('owner_payment/', views.owner_payment, name='owner_payment'),
    path('rating/<int:id>', views.rating, name='rating'),

]