from django.shortcuts import render
from django.views.generic import TemplateView 
from django.http import JsonResponse 
from .models import NetworkConnection,PortStatus,SecurityAlert,AnomalyDetectionModel 
from django.utils import timezone 
from datetime import timedelta 


# Create your views here.
class DashboardView(TemplateView): #class DashboardView extending django's TemplateView 
    template_name = "monitor/dashboard.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
        #getting recent alerts 
        context['recent_alerts']=SecurityAlert.objects.filter(
            is_resolved='False'

        ).order_by('-timestamp')[:10]

        context['port_status'] = PortStatus.objects.all().order_by('port_number')

        #get connection statistics 
        last_hour = timezone.now() - timedelta(hours=1)
        context['connection_count'] = NetworkConnection.objects.filter(
            timestamp__gte = last_hour
        ).count()

        return context