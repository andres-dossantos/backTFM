from django.urls import path, include

from rest_framework.routers import DefaultRouter
from predictions.views import PredictionViewSet

router = DefaultRouter()
router.register(r'predictions', PredictionViewSet, basename='predictions')
predictions_url_patterns = [path('', include(router.urls))]