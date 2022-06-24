from django.urls import path
from .import  views

urlpatterns=[
     path('', views.index, name='index'),
     path('register/',views.register, name='register'),
     path('user_register/',views.customer_register.as_view(), name='customer_register'),
     path('admin_register/',views.employee_register.as_view(), name='employee_register'),
     # path('',views.login_request, name='login'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
]