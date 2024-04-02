from django.urls import path
from .views import (
    PetDetailView,
    PetListView,
    PetCreateView,
    MePetsView,
    LastLocalUpdateView,
)

app_name = "pets"

urlpatterns = [
    path("create/", PetCreateView.as_view(), name="api-pets-create"),
    path("", PetListView.as_view(), name="api-pets-list"),
    path("me/", MePetsView.as_view(), name="api-me-pets"),
    path("<slug:slug>/", PetDetailView.as_view(), name="api-pets-detail"),
]

urlpatterns += [
    path(
        "<slug:slug>/lastlocal/",
        LastLocalUpdateView.as_view(),
        name="api-pets-lastlocal-update",
    ),
]
