from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreateView,
                          SuccessTemplateView, OrdersTemplateView,
                          OrderDetailView)

app_name = 'orders'

urlpatterns = [
    path('', OrdersTemplateView.as_view(),
         name='order_list'),
    path('create-order/', OrderCreateView.as_view(),
         name='create_order'),
    path('success-order/', SuccessTemplateView.as_view(),
         name='success_order'),
    path('canceled-order/', CanceledTemplateView.as_view(),
         name='canceled_order'),
    path('detail/<int:id>/', OrderDetailView.as_view(),
         name='order_detail'),
]
