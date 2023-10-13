from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from property import views as propertyViews


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', propertyViews.home, name='home'),
    path('property/', include('property.urls', namespace='property')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
