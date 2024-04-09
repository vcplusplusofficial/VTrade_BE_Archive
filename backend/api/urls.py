from django.urls import path
from .views import add_transaction_view, transaction_detail

urlpatterns = [
    path('transactions/add/', add_transaction_view, name='add_transaction'),
    path('transactions/detail/', transaction_detail, name='transaction_detail'),
]
