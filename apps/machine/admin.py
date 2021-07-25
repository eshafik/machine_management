from django.contrib import admin

# Register your models here.
from apps.machine.models import Machine, MachineData

admin.site.register(Machine)
admin.site.register(MachineData)
