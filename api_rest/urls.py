from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path(':<str:id>', views.transactions_manager),
    path('', views.transaction_list_create),
]