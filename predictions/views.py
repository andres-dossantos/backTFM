from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Prediction
from .serializers import PredictionSerializer, PredictionUploadSerializer
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

# Create your views here.


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        print(f"Request: {request.data}")
        print(f"File: {request.data['file']}")
        file = request.data.get('file', None)
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(file) # usar esta varible para llamar la funcion de prediccion
            print(f"DataFrame: {df}")
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
