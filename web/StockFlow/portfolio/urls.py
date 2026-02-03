from django.urls import path
from . import views

urlpatterns = [
    path("holdings", views.holding_list, name="holding_list"),
    path("holdings/create", views.holding_create, name="holding_create"),
    path("holdings/edit/<int:pk>", views.holding_edit, name="holding_edit"),
    path("holdings/delete/<int:pk>", views.holding_delete, name="holding_delete"),
    path("holdings/update", views.holding_update, name="holding_update"),
]

