from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.show_all_orders, name='orders'),
    path('own/', views.show_own_orders, name='order'),
    path('create/', views.create_an_order, name='new_order'),
    path('del/', views.del_order_by_root, name='del_order'),
    path('del/<int:order_id>', views.del_order_by_root, name='del_order'),
    path('update/<int:order_id>', views.upd_order, name='upd_order'),
]