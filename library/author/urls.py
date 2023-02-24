from django.urls import path, include
from . import views


urlpatterns = [
    path('create_author/', views.AuthorFormView.as_view(), name='create_author'),
    path('create_author/success/', views.success_author_creation, name='success'),
    path('delete/success/', views.success_author_deletion, name='success_del'),
    path('show_authors/', views.show_authors, name='show_authors'),
    path('remove_author/', views.remove_author, name='remove_author'),
    path('update/<int:author_id>', views.update_author, name='update_author'),
    path('delete/<int:author_id>', views.delete_author, name='delete_author'),
]
