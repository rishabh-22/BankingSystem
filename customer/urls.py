from django.urls import path
from rest_framework.authtoken import views

from customer.views import registration_view

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', views.obtain_auth_token, name='login'),

]
