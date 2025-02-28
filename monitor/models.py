from django.db import models
from django.utils import timezone 


# Create your models here.
# we have to create 4 models 
# 1 : Network Connection 
# 2 : Port Status 
# 3 : Security Alerts 
# 4 : Anomaly Detection Model 


#Model to store information of the packets 
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


class PortStatus(models.Model):
    port_number = models.IntegerField()
    status = models.CharField(max_length=20) #will indicate , if the port if open , closed or filtered
    service = models.CharField(max_length=100 , null=True , blank=True)
    
    last_checked = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['port_number']),
            models.Index(fields=['status']),
        ]


#Model for storing alerts when anomalies are detected 
class SecurityAlert(models.Model):
    SEVERITY_CHOICES = [
        ('LOW' , 'Low'),
        ('MEDIUM','Medium'),
        ('HIGH','High'),
        ('CRITICAL','Critical'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    severity = models.CharField(max_length=10 , choices=SEVERITY_CHOICES)
    source_ip = models.GenericIPAddressField(null=True , blank=True)
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(null=True , blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['severity']),
            models.Index(fields=['is_resolved']),
        ]


class AnomalyDetectionModel(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now)
    last_trained = models.DateTimeField(default=timezone.now)
    accuracy_score = models.FloatField(null=True , blank=True)
    model_file = models.FileField(upload_to='ml_models/')
    is_active = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
        ]


        