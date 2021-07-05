from django.urls import path
from . import views

app_name = 'qiwi_payment'

urlpatterns = [
    path('process/', views.payment_process, name='payment_process'),
    path('handler/success/', views.PaymentView.as_view(), name='payment_success')
]