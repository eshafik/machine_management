from django.urls import path

from apps.machine.views import MachineListAPI, MachineDataLisAPI, MachineDataAnalyticsAPI, MachineDataTotalAnalyticsAPI

# Put here views here
urlpatterns = [
    path('', MachineListAPI.as_view(), name='machine-list-api'),
    path('data', MachineDataLisAPI.as_view(), name='machine-data-list-api'),
    path('analytics', MachineDataAnalyticsAPI.as_view(), name='machine-data-analytics-api'),
    path('total-analytics', MachineDataTotalAnalyticsAPI.as_view(), name='machine-data-total-analytics-api'),
]
