from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .serializers import FormSerializer
from forms.models import Form


# Create your views here.

class FormViewSet(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = FormSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__id']

    def get_queryset(self):
        return Form.objects.all().order_by('user__username')
