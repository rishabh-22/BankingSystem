from django.urls import path
from rest_framework.authtoken import views

from customer.views import registration_view, add_transaction, view_transaction

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', views.obtain_auth_token, name='login'),
    path('transaction/add/', add_transaction, name='add_transaction'),
    path('transaction/view/', view_transaction, name='view_transaction'),

]
