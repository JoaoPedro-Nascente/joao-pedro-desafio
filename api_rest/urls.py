from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path(':<str:id>', views.get_transactions_by_id),
]