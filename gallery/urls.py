from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('delete/<int:pk>/', views.delete_photo, name='delete_photo'),
    path('edit/<int:pk>/', views.update_photo, name='edit_photo'),
]