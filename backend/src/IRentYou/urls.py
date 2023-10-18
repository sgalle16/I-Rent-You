from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.contrib import admin
from django.urls import path, include
from property.views import (PropertyListView, PropertyDetailView, PropertyCreateView,
                            PropertyUpdateView,PropertyDeleteView)

from django import views
from Users.views import register_view , login_view ,CustomPasswordChangeView , home , logoutaccount , view_and_edit_profile , confirm_delete_account , notification_list



urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home ,name="home"),

    path('accounts/', include('allauth.urls')),
    path('', PropertyListView.as_view(), name="property-list"),
    path('create_property/', PropertyCreateView.as_view(), name="property-create"),

    
    path('login/', login_view  , name="login"),
    path('register/', register_view , name="register"),   
    path('logoutaccount/', logoutaccount , name="salir"),    
    path('perfil/', view_and_edit_profile , name="perfil"),
    path('noficaciones/', view_and_edit_profile , name="notificaciones"),
    path('perfil/confirm-delete-account/',confirm_delete_account , name='confirm-delete-account'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('notification/',notification_list , name='notify'),
    

    path('property/<int:pk>/detail/', PropertyDetailView.as_view(), name="property-detail"),
    path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name="property-update"),
    path('property/<int:pk>/delete/', PropertyDeleteView.as_view(), name="property-delete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
