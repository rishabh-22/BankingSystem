from django.urls import path
from rest_framework.authtoken import views

from customer.views import registration_view, add_transaction, view_transaction, view_account, view_balance, \
    filter_transactions

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', views.obtain_auth_token, name='login'),
    path('transaction/add/', add_transaction, name='add_transaction'),
    path('transaction/view/', view_transaction, name='view_transaction'),
    path('transaction/filter/', filter_transactions, name='filter_transactions'),
    path('account/view/', view_account, name='view_account'),
    path('account/balance/', view_balance, name='view_balance'),
]
