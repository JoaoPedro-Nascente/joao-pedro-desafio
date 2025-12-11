from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('auth/', include('api_rest.auth.urls')),

    path('transactions/', include('api_rest.transactions.urls'))
]