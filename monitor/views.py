# from django.shortcuts import render
# from django.views.generic import TemplateView 
# from django.http import JsonResponse 
# from .models import NetworkConnection,PortStatus,SecurityAlert,AnomalyDetectionModel 
# from django.utils import timezone 
# from datetime import timedelta 


# # Create your views here.
# class DashboardView(TemplateView): #class DashboardView extending django's TemplateView 
#     template_name = "monitor/dashboard.html"

#     def get_context_data(self, **kwargs):
#         return super().get_context_data(**kwargs)
    
#         #getting recent alerts 
#         context['recent_alerts']=SecurityAlert.objects.filter(
#             is_resolved='False'

#         ).order_by('-timestamp')[:10]

#         context['port_status'] = PortStatus.objects.all().order_by('port_number')

#         #get connection statistics 
#         last_hour = timezone.now() - timedelta(hours=1)
#         context['connection_count'] = NetworkConnection.objects.filter(
#             timestamp__gte = last_hour
#         ).count()

#         return context


from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

from .models import NetworkConnection, PortStatus, SecurityAlert, AnomalyDetectionModel
from .services.port_scanner import PortScanner

# Dashboard view
class DashboardView(TemplateView):
    template_name = "monitor/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Getting recent alerts 
        context['recent_alerts'] = SecurityAlert.objects.filter(
            is_resolved=False
        ).order_by('-timestamp')[:10]

        context['port_status'] = PortStatus.objects.all().order_by('port_number')

        # Get connection statistics 
        last_hour = timezone.now() - timedelta(hours=1)
        context['connection_count'] = NetworkConnection.objects.filter(
            timestamp__gte=last_hour
        ).count()

        return context

# Alert views
class AlertListView(ListView):
    model = SecurityAlert
    template_name = 'monitor/alerts.html'
    context_object_name = 'alerts'
    paginate_by = 20
    
    def get_queryset(self):
        return SecurityAlert.objects.all().order_by('-timestamp')
    
    def render_to_response(self, context, **kwargs):
        # If it's an AJAX request, return JSON
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            alerts = list(context['object_list'].values(
                'id', 'title', 'description', 'timestamp', 'severity', 'source_ip', 'is_resolved'
            ))
            for alert in alerts:
                alert['timestamp'] = alert['timestamp'].isoformat()
            
            return JsonResponse({'alerts': alerts})
        
        # Otherwise, return the normal template response
        return super().render_to_response(context, **kwargs)

class AlertDetailView(DetailView):
    model = SecurityAlert
    template_name = 'monitor/alert_detail.html'
    context_object_name = 'alert'

# Port status view
class PortStatusView(ListView):
    model = PortStatus
    
    def render_to_response(self, context, **kwargs):
        ports = list(PortStatus.objects.all().values(
            'id', 'port_number', 'status', 'service', 'last_checked'
        ))
        for port in ports:
            port['last_checked'] = port['last_checked'].isoformat()
        
        return JsonResponse({'ports': ports})

# Connection stats view
class ConnectionStatsView(View):
    def get(self, request, *args, **kwargs):
        timeframe = request.GET.get('timeframe', 'hour')
        
        if timeframe == 'hour':
            start_time = timezone.now() - timedelta(hours=1)
        elif timeframe == 'day':
            start_time = timezone.now() - timedelta(days=1)
        elif timeframe == 'week':
            start_time = timezone.now() - timedelta(weeks=1)
        else:
            start_time = timezone.now() - timedelta(hours=1)
        
        # Get connection counts
        connections = NetworkConnection.objects.filter(
            timestamp__gte=start_time
        )
        
        # Group by 5-minute intervals
        interval = 5 * 60  # 5 minutes in seconds
        stats = {}
        
        for conn in connections:
            # Round down to nearest 5-minute interval
            timestamp = conn.timestamp.timestamp()
            interval_timestamp = int(timestamp / interval) * interval
            interval_key = timezone.datetime.fromtimestamp(interval_timestamp).isoformat()
            
            if interval_key not in stats:
                stats[interval_key] = 0
            
            stats[interval_key] += 1
        
        # Format for chart
        chart_data = [{'time': k, 'count': v} for k, v in stats.items()]
        chart_data.sort(key=lambda x: x['time'])
        
        return JsonResponse({'data': chart_data})

# Function to resolve alerts (removed login_required)
def resolve_alert(request, pk):
    alert = get_object_or_404(SecurityAlert, pk=pk)
    
    if request.method == 'POST':
        alert.is_resolved = True
        alert.resolution_notes = request.POST.get('notes', '')
        alert.save()
        
        return redirect('monitor:alerts')
    
    return redirect('monitor:alert_detail', pk=pk)

# Function to trigger port scan (removed csrf_exempt and login_required)
def trigger_scan(request):
    if request.method == 'POST':
        scanner = PortScanner()
        scanner.scan_common_ports()
        
        return JsonResponse({'status': 'success', 'message': 'Port scan completed'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)