from django.db import models
from users.models import User
# Create your models here.


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ten_km_time = models.FloatField()
    half_marathon_time = models.FloatField()
    marathon_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
