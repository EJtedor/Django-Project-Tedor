"""
URL configuration for nasa_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from accounts.views import register

# Redirect the root URL to the astronauts list view
def home(request):
    return redirect('astronaut_list')  # Ensure 'astronaut_list' is defined in astronauts/urls.py

urlpatterns = [
    path('', home, name='home'),  # Redirect the root URL
    path('admin/', admin.site.urls),  # Django admin route
    path('astronauts/', include('astronauts.urls')),  # Include astronauts app URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),  # Logout view
    path('register/', register, name='register'),  # Registration route
    path('api/', include('astronauts.api.urls')),  # Include API routes
]


