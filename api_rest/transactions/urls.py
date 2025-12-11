from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path('<uuid:id>/', views.transactions_manager, name='transactions_manager'),
    path('', views.transaction_list_create, name='transaction_list_create'),
    path('summary/', views.summary_view, name='summary_view')
]