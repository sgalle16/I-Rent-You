from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from property.views import (PropertyListView, PropertyDetailView, PropertyCreateView,
                            PropertyUpdateView,PropertyDeleteView, PropertyFeatureCreateView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', PropertyListView.as_view(), name="property-list"),
    path('create_property/', PropertyCreateView.as_view(), name="property-create"),
    path('property/<int:pk>/detail/', PropertyDetailView.as_view(), name="property-detail"),
    path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name="property-update"),
    path('property/<int:pk>/delete/', PropertyDeleteView.as_view(), name="property-delete"),

    path('property/<int:pk>/add_feature/', PropertyFeatureCreateView.as_view(), name="add-feature")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
