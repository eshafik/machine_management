from rest_framework import serializers

from apps.machine.models import MachineData, Machine


class MachineDataSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(source='created_at')
    end = serializers.DateTimeField(source='updated_at')

    class Meta:
        model = MachineData
        fields = ('machine_no', 'machine_status', 'start', 'end', 'total_minutes')


class MachineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ('machine_no', 'name')
