from django.urls import path
from . import views

urlpatterns = [
    path("assets/", views.asset_list, name="asset_list"),
    path("assets/create/", views.asset_create, name="asset_create"),
    path("assets/edit/<int:pk>/", views.asset_edit, name="asset_edit"),
    path("assets/delete/<int:pk>/", views.asset_delete, name="asset_delete"),
    path("assets/update/", views.asset_update, name="asset_update"),
]

