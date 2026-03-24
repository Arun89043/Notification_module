from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view()),
    path("create/", views.create_notification_view),
    path("<uuid:pk>/read/", views.MarkNotificationReadView.as_view()),

    # test APIs
    path("test-payment/", views.test_payment),
    path("test-delivery/", views.test_delivery),
    path("test-payout/", views.test_payout),
]