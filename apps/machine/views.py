from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from app_libs.success_codes import SUCCESS_CODE
from app_libs.error_codes import ERROR_CODE
from apps.machine.models import Machine, MachineData
from apps.machine.serializers import MachineDataSerializer


class MachineListAPI(APIView):

    model_name = Machine

    def get(self, request):
        machines = Machine.objects.filter(status=True
                                          ).values('name', 'machine_no') or {"message": "Status OK",
                                                                             "success": True, "data": []}
        return Response(data=machines, status=status.HTTP_200_OK)


class MachineDataLisAPI(ListAPIView):
    model_name = MachineData
    serializer_class = MachineDataSerializer
    queryset = MachineData.objects.filter()

    def get_queryset(self):
        params = self.request.query_params.dict()
        queryset = self.queryset
        if params.get('status'):
            ids = self.queryset.order_by('machine_no', '-id').distinct('machine_no').values('id')
            time_to_online = timezone.now() - timezone.timedelta(minutes=8)
            if params.get('status') == 'online':
                return queryset.filter(id__in=ids, updated_at__gt=time_to_online)
            else:
                return queryset.filter(id__in=ids, updated_at__lt=time_to_online)
        if params.get('start'):
            queryset = queryset.filter(Q(created_at__gte=params.get('start')
                                         ) | Q(updated_at__gte=params.get('start')))
        if params.get('end'):
            queryset = queryset.filter(updated_at__lte=params.get('end'))
        if params.get('machine_no'):
            machines = params.get('machine_no').split('-')
            queryset = queryset.filter(machine_no__in=machines)
        if params.get('machine_status'):
            queryset = queryset.filter(machine_status__iexact=params.get('machine_status'))
        if not params.get('start'):
            last_seven_days = timezone.now() - timezone.timedelta(days=7)
            queryset = queryset.filter(created_at__gt=last_seven_days)
        return queryset
