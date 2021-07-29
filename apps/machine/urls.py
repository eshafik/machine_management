from django.urls import path

from apps.machine.views import MachineListAPI, MachineDataLisAPI

# Put here views here
urlpatterns = [
    path('', MachineListAPI.as_view(), name='machine-list-api'),
    path('data', MachineDataLisAPI.as_view(), name='machine-data-list-api'),
]
