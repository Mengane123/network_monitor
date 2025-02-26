from django.db import models
from django.utils import timezone 


# Create your models here.
# we have to create 4 models 
# 1 : Network Connection 
# 2 : Port Status 
# 3 : Security Alerts 
# 4 : Anomaly Detection Model 


class NetworkConnection(models.Model):
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    source_port = models.IntegerField()
    destination_port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)
    bytes_transferred = models.BigIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(field=['source_ip']),
            models.Index(field=['destination_ip']),
        ]


