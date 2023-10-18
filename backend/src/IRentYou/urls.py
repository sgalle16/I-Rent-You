from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from property.views import (PropertyListView, PropertyDetailView, PropertyCreateView,
                            PropertyUpdateView,PropertyDeleteView)

from django import views
from Users.views import register_view , login_view , home , logoutaccount


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home ,name="home"),

    path('accounts/', include('allauth.urls')),
    path('', PropertyListView.as_view(), name="property-list"),
    path('create_property/', PropertyCreateView.as_view(), name="property-create"),

    #path('logout/', CustomUserCreationForm.as_view(), name="logout"),
    path('login/', login_view  , name="login"),
    path('register/', register_view , name="register"),   
    path('logoutaccount/', logoutaccount , name="salir"),    
    path('perfil/', home , name="perfil"),    

    path('property/<int:pk>/detail/', PropertyDetailView.as_view(), name="property-detail"),
    path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name="property-update"),
    path('property/<int:pk>/delete/', PropertyDeleteView.as_view(), name="property-delete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
