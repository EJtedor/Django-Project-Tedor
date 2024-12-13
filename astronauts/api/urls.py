from django.urls import path
from .api_views import AstronautListAPIView  # Ensure this imports correctly

urlpatterns = [
    path('astronauts/', AstronautListAPIView.as_view(), name='astronaut-list'),
]
