from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Notification
from .serializers import NotificationSerializer
from .services import (
    create_notification,
    trigger_payment_received,
    trigger_delivery_update,
    trigger_payout_processed
)


# ✅ LIST NOTIFICATIONS
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


# ❌ REMOVE OLD CreateAPIView (it bypasses SMS)
# class NotificationCreateView(generics.CreateAPIView):
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# ✅ CREATE NOTIFICATION (WITH SMS)
@api_view(['POST'])
def create_notification_view(request):
    user = request.user
    notification_type = request.data.get("type")

    notification = create_notification(
        user=user,
        notification_type=notification_type
    )

    return Response({
        "message": "Notification created",
        "id": notification.id
    })


# ✅ MARK AS READ
class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(
                pk=pk,
                user=request.user
            )
            notification.is_read = True
            notification.save()

            return Response({"message": "Notification marked as read"})

        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)


# ✅ TEST APIs (AUTO TRIGGERS)

def test_payment(request):
    user = User.objects.get(id=2)
    trigger_payment_received(user)

    return JsonResponse({
        "message": "Payment + Notification Triggered"
    })


def test_delivery(request):
    user = User.objects.get(id=2)
    trigger_delivery_update(user)

    return JsonResponse({
        "message": "Delivery + Notification Triggered"
    })


def test_payout(request):
    user = User.objects.get(id=2)
    trigger_payout_processed(user)

    return JsonResponse({
        "message": "Payout + Notification Triggered"
    })