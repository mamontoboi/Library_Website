"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_view
from author import views as author_view
from book import views as book_view
from order import views as order_view
from rest_framework import routers
from author.views import AuthorAPIView
from authentication.views import UserAPIView

author_router = routers.DefaultRouter()
author_router.register('', AuthorAPIView)

user_router = routers.DefaultRouter()
user_router.register('', UserAPIView)
# `http://127.0.0.1:8000/api/v1/user/{id}?`
# `http://127.0.0.1:8000/api/v1/user/{id}/order/{id}?`
# `http://127.0.0.1:8000/api/v1/order/{id}?`
# `http://127.0.0.1:8000/api/v1/book/{id}?`
# `http://127.0.0.1:8000/api/v1/author/{id}?`


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls', namespace='book')),
    path('authentication/', include(('authentication.urls', 'authentication'),
                                    namespace='authentication')),
    path('author/', include(('author.urls', 'author'), namespace='author')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
    path('', include(('authentication.urls', 'main_page'),
                     namespace='main_page')),
    path('api/v1/book/', book_view.BookList.as_view(), name='book-list'),
    path('api/v1/book/<int:pk>/', book_view.BookInfo.as_view(), name='book-detail'),
    path('api/v1/book/create/', book_view.BookCreate.as_view(), name='book-create'),
    path('api/v1/order/create/', order_view.CreateOrder.as_view(), name='order-create'),
    path('api/v1/order/', order_view.OrderList.as_view(), name='order-list'),
    path('api/v1/order/<int:pk>/', order_view.OrderCRUD.as_view(), name='order-detail'),
    path('api/v1/user/<int:user_id>/order/<int:order_id>/', order_view.UserOrder.as_view(), name='specific-order'),
    path('api/v1/user/<int:user_id>/order/', order_view.UserOrderList.as_view({'get': 'list'}),
         name='all_orders_of_user'),
    path('api/v1/author/', include(author_router.urls)),
    path('api/v1/user/', include(user_router.urls)),
]
