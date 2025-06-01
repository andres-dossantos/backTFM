from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'user', 'ten_km_time', 'half_marathon_time', 'marathon_time', 'created_at', 'updated_at']


class PredictionUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("The file must be a CSV file")
        return value

