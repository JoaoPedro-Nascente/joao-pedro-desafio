from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('transactions/:<str:id>', views.transactions_manager),
    path('transactions/', views.transaction_list_create),
    path('summary/', views.summary_view)
]