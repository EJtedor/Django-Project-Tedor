from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.astronaut_dashboard, name='astronaut_dashboard'),  # Dashboard root
    path('missions/', views.mission_list, name='mission_list'),  # List all missions
    path('missions/<int:pk>/', views.mission_detail, name='mission_detail'),  # Mission details
    path('missions/new/', views.mission_create, name='mission_create'),  # Create a new mission
    path('missions/<int:pk>/edit/', views.mission_update, name='mission_update'),  # Update an existing mission
    path('missions/<int:pk>/delete/', views.mission_delete, name='mission_delete'),  # Delete a mission
    path('bmi/', views.bmi_list, name='bmi_list'),
    path('bmi/new/', views.bmi_create, name='bmi_create'),
    path('bmi/<int:pk>/edit/', views.bmi_update, name='bmi_update'),    path('bmi/<int:pk>/delete/', views.bmi_delete, name='bmi_delete'),
    path('bmi/records/', views.bmi_records, name='bmi_records'),
    path('bmi_calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('save_records/', views.save_records, name='save_records'),
    path('missions/', views.mission_list, name='missions_list'),
    path('api/astronauts/', include('astronauts.api.urls')),  # Include API routes
]
