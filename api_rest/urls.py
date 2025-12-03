from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path(':<str:id>', views.transactions_manager),
    path('', views.create_new_transaction),
]