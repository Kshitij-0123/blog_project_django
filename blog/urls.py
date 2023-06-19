from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
