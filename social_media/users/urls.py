from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (UserRegisterView, UserPostsView, AddFollowerView, RemoveFollowerView, 
    UserProfileSearchView, FollowersListView, PostNotificationView, FollowNotificationView
)
from django.contrib.auth import views 



urlpatterns= [
    path('register/', UserRegisterView.as_view(), name= 'register'),
    path('login/', views.LoginView.as_view(template_name= 'users/login.html'), name= 'login'),
    path('logout/', views.LogoutView.as_view(template_name= 'users/logout.html'), name= 'logout'),
   
   
    # adding password reset functionality to the social media appp
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name= 'users/password_reset.html'), name= 'password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name= 'users/password_reset_done.html'), name= 'password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name= 'users/password_reset_confirm.html'), name= 'password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name= 'users/password_reset_complete.html'), name= 'password_reset_complete'),


    path('<str:username>/followers/add/', AddFollowerView.as_view(), name= 'add-follower'),
    path('<str:username>/followers/remove/', RemoveFollowerView.as_view(), name= 'remove-follower'),
    path('<str:username>/followers/', FollowersListView.as_view(), name= 'followers-list'),
    path('<str:username>/posts/', UserPostsView.as_view(), name= 'user-posts'), 
    path('search/', UserProfileSearchView.as_view(), name= 'profile-search'),
    path('notifications/<int:notification_pk>/post/<int:post_pk>/', PostNotificationView.as_view(), name= 'post-notification'),
    path('notifications/<int:notification_pk>/profile/<str:username>/', FollowNotificationView.as_view(), name= 'follower-notification'),
]