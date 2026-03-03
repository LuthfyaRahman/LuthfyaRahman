import structlog
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GratifikasiRecordSerializer, GratifikasiSubmitSerializer
from .services import create_record
from .tasks import call_ai_predict

logger = structlog.get_logger(__name__)


class SubmitRecordView(APIView):
    """
    POST /api/submit
    Accept a gratification description, persist it, and trigger async AI analysis.
    """

    permission_classes = []  # Public endpoint; add auth for production

    def post(self, request: Request) -> Response:
        serializer = GratifikasiSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        record = create_record(
            text=serializer.validated_data["text"],
            value_estimation=serializer.validated_data.get("value_estimation"),
        )

        # Fire-and-forget Celery task
        call_ai_predict.delay(record.pk, record.text)

        logger.info("record_submitted", record_id=record.pk)
        return Response(
            GratifikasiRecordSerializer(record).data,
            status=status.HTTP_202_ACCEPTED,
        )


class HealthCheckView(APIView):
    """GET /api/health — lightweight liveness probe."""

    permission_classes = []

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})
