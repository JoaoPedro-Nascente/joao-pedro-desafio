from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('transactions/<uuid:id>/', views.transactions_manager, name='transactions_manager'),
    path('transactions/', views.transaction_list_create, name='transaction_list_create'),
    path('summary/', views.summary_view, name='summary_view')
]