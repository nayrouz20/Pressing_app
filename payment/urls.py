from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name="process_order"),
    path('delivered_dash/', views.delivered_dash, name="delivered_dash"),
    path('not_delivered_dash/' ,views.not_delivered_dash, name="not_delivered_dash"),
    path('orders/<int:pk>/', views.orders, name='orders'),
    path('order_status/', views.order_status, name='order_status'),
    path("get_orders_status/", views.get_orders_status, name="get_orders_status"),

]