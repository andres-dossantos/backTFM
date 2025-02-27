from rest_framework import serializers
from forms.models import Form


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'

class ResultSerializer(serializers.Serializer):
    pais = serializers.CharField()
    continente = serializers.CharField()
    score = serializers.FloatField()