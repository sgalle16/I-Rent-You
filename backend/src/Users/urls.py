from django.urls import path

from Users.views import (register_view, login_view, CustomPasswordChangeView, logoutaccount, view_and_edit_profile, confirm_delete_account, notification_list)

from property.views import LessorPropertyListView

app_name = 'Users'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logoutaccount/', logoutaccount, name="logout"),
    path('profile/', view_and_edit_profile, name="profile"),
    path('notifications/', view_and_edit_profile, name="notifications"),
    path('profile/confirm-delete-account/', confirm_delete_account, name='confirm-delete-account'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('notification/', notification_list, name='notify'),
    
    path("lessor/", LessorPropertyListView.as_view(), name="lessor-properties"),

]
