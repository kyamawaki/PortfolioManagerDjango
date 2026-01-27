from django.urls import path
from . import views

urlpatterns = [
    # Execute views.assete_list() when the /assets/ URL is accessed.
    path("assets/", views.asset_list, name="asset_list"),
    path("assets/new/", views.asset_create, name="asset_create"),
    path("assets/<int:pk>/edit/", views.asset_edit, name="asset_edit"),
    path("assets/<int:pk>/delete/", views.asset_delete, name="asset_delete"),
    #path("portfolio/", views.portfolio_list, name="portfolio_list"),
    path("portfolio/holdings", views.holding_list, name="holdings_list"),
    path("portfolio/add", views.add_holding, name="add_holding"),
]

