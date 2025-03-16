from django.contrib import admin
from django.urls import path, include
from login.views import *
from app.views import *
from dashboard.views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login', include('login.urls')),
    path('dashboard', dashView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
]
