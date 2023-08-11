from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('display_menu/', views.display_menu, name='display_menu'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('take_order/', views.take_order, name='take_order'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('admin_section/', views.admin_section, name='admin_section'),
    path('user_section/', views.user_section, name='user_section'),
    path('review_orders/', views.review_orders, name='review_orders'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('remove_dish/', views.remove_dish, name='remove_dish'),
    path('update_dish_availability/', views.update_dish_availability, name='update_dish_availability'),
      path('user_logout/', views.user_logout, name='user_logout'),
        path('admin_menu/', views.admin_menu, name='admin_menu'),
         path('admin_logout/', views.admin_logout, name='admin_logout')
]