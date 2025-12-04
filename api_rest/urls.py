from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
    path('register/', views.register_user, name='user_register'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('transactions/<uuid:id>/', views.transactions_manager, name='transactions_manager'),
    path('transactions/', views.transaction_list_create, name='transaction_list_create'),
    path('summary/', views.summary_view, name='summary_view')
]