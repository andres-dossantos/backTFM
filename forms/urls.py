from django.urls import path, include

from rest_framework.routers import DefaultRouter
from forms.views import FormViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet, basename='forms')
forms_url_patterns = [path('', include(router.urls))]