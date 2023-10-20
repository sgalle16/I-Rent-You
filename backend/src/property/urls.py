from django.urls import path

from property.views import (PropertyListView, PropertyDetailView, PropertyCreateView, PropertySearchListView,
                            PropertyUpdateView, PropertyDeleteView)


app_name = 'property'

urlpatterns = [
    path('', PropertyListView.as_view(), name="list"),
    path('create/', PropertyCreateView.as_view(), name="create"),
    path('<int:pk>/detail/', PropertyDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', PropertyUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name="delete"),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name="delete"),
    path('search/', PropertySearchListView.as_view(), name="search"),
]
