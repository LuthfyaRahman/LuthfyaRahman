from django.urls import path

from .views import HealthCheckView, SubmitRecordView

urlpatterns = [
    path("submit", SubmitRecordView.as_view(), name="submit-record"),
    path("health", HealthCheckView.as_view(), name="health-check"),
]
