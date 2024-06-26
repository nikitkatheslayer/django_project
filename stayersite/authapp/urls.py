from django.urls import path
from authapp import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('checkpass/', views.check_pass, name='check_pass')
]