from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete-category'),
]
