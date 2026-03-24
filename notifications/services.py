from .models import Notification
from .sms_service import send_notification_sms


def create_notification(user, notification_type, reference_id=None):
    """
    Create notification + send SMS
    """

    # Auto title + message based on type
    if notification_type == Notification.NotificationType.SHIPMENT_ASSIGNED:
        title = "Shipment Assigned"
        message = "A shipment has been assigned to you."

    elif notification_type == Notification.NotificationType.DELIVERY_UPDATE:
        title = "Delivery Status Updated"
        message = "Your shipment delivery status has been updated."

    elif notification_type == Notification.NotificationType.PAYMENT_RECEIVED:
        title = "Payment Received"
        message = "Payment has been successfully received."

    elif notification_type == Notification.NotificationType.PAYOUT_PROCESSED:
        title = "Payout Processed"
        message = "Your payout has been processed."

    else:
        title = "Notification"
        message = "You have a new notification."

    # ✅ Create notification in DB
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=notification_type,
        reference_id=reference_id
    )

    print("Notification auto triggered:", title)

    # ✅ Send SMS
    try:
        send_notification_sms(user, message)
    except Exception as e:
        print("SMS Error:", e)

    return notification


# 🔥 Trigger functions
def trigger_delivery_update(user):
    return create_notification(
        user=user,
        notification_type=Notification.NotificationType.DELIVERY_UPDATE
    )


def trigger_payment_received(user):
    return create_notification(
        user=user,
        notification_type=Notification.NotificationType.PAYMENT_RECEIVED
    )


def trigger_payout_processed(user):
    return create_notification(
        user=user,
        notification_type=Notification.NotificationType.PAYOUT_PROCESSED
    )