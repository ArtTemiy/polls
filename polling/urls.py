from django.urls import path, include

urlpatterns = [
    path('api/', include('polling.api_urls')),
]