from django.contrib import admin
from django.urls import path, include
from login.views import *
from app.views import *
from dashboard.views import *
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('', include('login.urls')),
    path('dashboard', dashView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
]
