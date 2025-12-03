from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/', include('api_rest.urls'), name='api_rest_urls'),
]