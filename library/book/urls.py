from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.list_books, name='books'),
    path('<int:book_id>', views.detail, name='book_detail'),
    path('user_book/<int:user_id>', views.show_book_for_specific_user, name='user_detail_book'),
    path('create_book/', views.create_book, name='create_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('success_book_creation/<str:name>', views.success_book_creation, name='success_book'),
    path('success_book_deletion/', views.success_book_deletion, name='success_delete_book'),
    path('update/<int:book_id>', views.update_book, name='update_book'),
]
