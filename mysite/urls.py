from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Agora Route
    path('', include('agora.urls')),
    path('admin/', admin.site.urls),
]