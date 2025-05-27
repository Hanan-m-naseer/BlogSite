from django.urls import path
from .views import register_view,home_view, update_profile_view,main_view
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('register/', views.register_view, name='register'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile_update/', views.update_profile_view, name='profile_update'),

    path('main/', views.main_view, name='main'),
    path('create/', views.create_post, name='create_post'),
    
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('main/', views.main_view, name='main'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),


]