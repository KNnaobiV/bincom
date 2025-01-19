from django.urls import path
from .views import (
    AddPartyResultsView,
    LGATotalResultsView,
    PollingUnitCreateView,
    PollingUnitResultView,
)

urlpatterns = [
    path(
        "add-party-result/<int:pk>/",
        AddPartyResultsView.as_view(),
        name="add-party-result"
    ),
    path(
        "lga-results/",
    LGATotalResultsView.as_view(),
        name="lga-results",
    ),
    path(
        "create-polling-unit/",
        PollingUnitCreateView.as_view(),
        name="create-polling-unit"
    ),
    path(
        "polling-unit/<int:pk>/",
        PollingUnitResultView.as_view(),
        name="polling_unit_result"
    ),
]