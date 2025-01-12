"""
URL configuration for novapulse project.

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

from novapulse.constants import SERVICE_NAME

urlpatterns = [
    path(f'{SERVICE_NAME}/admin/', admin.site.urls),
    path(f'{SERVICE_NAME}/grappelli/', include('grappelli.urls')),
    path(f'{SERVICE_NAME}/', include('apps.arbitrage_scanner.urls')),
]
