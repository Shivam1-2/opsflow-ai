from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import CanViewOrganizationRequests, IsOperatorOrAdmin
from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer
from apps.core.exceptions import InvalidStateTransitionError
from apps.requests.models import Request
from apps.requests.serializers import (
    RequestCreateSerializer,
    RequestDetailSerializer,
    RequestListSerializer,
    RequestStatusSerializer,
    RequestTransitionSerializer,
)
from apps.requests.services import RequestWorkflowService


def organization_requests(user):
    return Request.objects.filter(organization=user.organization).select_related(
        "created_by",
        "organization",
    )


class RequestPagination(PageNumberPagination):
    page_size = 20


class RequestListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsOperatorOrAdmin()]
        return [IsAuthenticated(), CanViewOrganizationRequests()]

    def get(self, request):
        queryset = organization_requests(request.user)
        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        paginator = RequestPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = RequestListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_obj = RequestWorkflowService.create_request(
            user=request.user,
            raw_text=serializer.validated_data["raw_text"],
            priority=serializer.validated_data.get("priority"),
        )
        return Response(
            RequestDetailSerializer(request_obj).data,
            status=status.HTTP_201_CREATED,
        )

class RequestDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewOrganizationRequests]

    def get(self, request, request_id):
        request_obj = get_object_or_404(organization_requests(request.user), pk=request_id)
        return Response(RequestDetailSerializer(request_obj).data)


class RequestStatusView(APIView):
    permission_classes = [IsAuthenticated, CanViewOrganizationRequests]

    def get(self, request, request_id):
        request_obj = get_object_or_404(organization_requests(request.user), pk=request_id)
        return Response(RequestStatusSerializer(request_obj).data)


class RequestTransitionView(APIView):
    permission_classes = [IsAuthenticated, IsOperatorOrAdmin]

    def post(self, request, request_id):
        request_obj = get_object_or_404(organization_requests(request.user), pk=request_id)
        serializer = RequestTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            updated = RequestWorkflowService.transition(
                request_obj=request_obj,
                user=request.user,
                target_status=serializer.validated_data["to_status"],
            )
        except InvalidStateTransitionError as exc:
            return Response(exc.detail, status=exc.status_code)
        return Response(RequestDetailSerializer(updated).data)


class RequestAuditListView(ListAPIView):
    permission_classes = [IsAuthenticated, CanViewOrganizationRequests]
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        request_obj = get_object_or_404(
            organization_requests(self.request.user),
            pk=self.kwargs["request_id"],
        )
        return (
            AuditLog.objects.filter(
                organization=self.request.user.organization,
                request=request_obj,
            )
            .select_related("actor")
            .order_by("-created_at")
        )
