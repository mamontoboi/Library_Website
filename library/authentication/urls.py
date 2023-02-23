from django.urls import path
from django.contrib.auth import views
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/<int:user_id>/', views.change_password,
         name='change_password'),
    path('users/all/', views.show_all_users, name='users'),
    path('users/', views.role_of_user, name='specific_user'),
    path('users/update_user/<int:user_id>/',
         views.update_user, name='update_user'),
    path('users/del_user/<int:user_id>/',
         views.del_user, name='del_user'),
    path('', views.main, name='main'),

]
