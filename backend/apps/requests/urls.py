from django.urls import path

from apps.requests.views import (
    RequestAuditListView,
    RequestDetailView,
    RequestListCreateView,
    RequestStatusView,
    RequestTransitionView,
)

urlpatterns = [
    path("", RequestListCreateView.as_view(), name="request-list-create"),
    path("<uuid:request_id>/", RequestDetailView.as_view(), name="request-detail"),
    path("<uuid:request_id>/status/", RequestStatusView.as_view(), name="request-status"),
    path(
        "<uuid:request_id>/transitions/",
        RequestTransitionView.as_view(),
        name="request-transition",
    ),
    path("<uuid:request_id>/audit/", RequestAuditListView.as_view(), name="request-audit"),
]
