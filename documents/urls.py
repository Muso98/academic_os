from django.urls import path
from . import views

urlpatterns = [
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),

    # Reports
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<uuid:report_id>/update/', views.report_update_status, name='report_update_status'),
]
