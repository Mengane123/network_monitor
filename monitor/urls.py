from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'monitor'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='monitor:dashboard'), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('alerts/', views.AlertListView.as_view(), name='alerts'),
    path('alerts/<int:pk>/', views.AlertDetailView.as_view(), name='alert_detail'),
    path('alerts/<int:pk>/resolve/', views.resolve_alert, name='resolve_alert'),
    path('port-status/', views.PortStatusView.as_view(), name='port_status'),
    path('connection-stats/', views.ConnectionStatsView.as_view(), name='connection_stats'),
    path('trigger-scan/', views.trigger_scan, name='trigger_scan'),
]