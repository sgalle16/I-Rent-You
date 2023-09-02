"""
URL configuration for IRentYou project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from property.views import (PropertyListView, PropertyDetailView, PropertyCreateView,
                            PropertyUpdateView,PropertyDeleteView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', PropertyListView.as_view(), name="property-list"),
    path('<slug>/', PropertyDetailView.as_view(), name="property-detail"),
    path('<slug>/update/', PropertyUpdateView.as_view(), name="property-update"),
    path('<slug>/delete/', PropertyDeleteView.as_view(), name="property-delete"),
    path('create/', PropertyCreateView.as_view(), name="property-create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
