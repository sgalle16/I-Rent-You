from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.contrib import admin
from django.urls import path, include
from Users import views as userViews


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    path('', userViews.home, name='home'),
    path('about/', userViews.about, name='about'),

    # URLs from the `Users` app
    path('', include('Users.urls', namespace='user')),


    # URLs from the `property` app
    path('property/', include('property.urls', namespace='property')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
