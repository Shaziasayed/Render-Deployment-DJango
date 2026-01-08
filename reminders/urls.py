from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, record_transaction, send_reminder, google_auth

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename="customers")

urlpatterns = [
    path("auth/google/", google_auth),
    path("record_transaction/", record_transaction),
    path("send-reminder/<int:customer_id>/", send_reminder),
    path("", include(router.urls)),
]
