from django.urls import path
from mainapp import views

urlpatterns = [
    path('', views.index),
    path('contact/', views.contact),
    path('products/', views.products),
]