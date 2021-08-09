from django.utils.decorators import method_decorator
from django.db.models import Q, Case, When, F, Sum, Value, IntegerField
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from app_libs.custom_pagination import CustomPagination
from app_libs.success_codes import SUCCESS_CODE
from app_libs.error_codes import ERROR_CODE
from apps.machine.models import Machine, MachineData
from apps.machine.serializers import MachineDataSerializer, MachineListSerializer


class MachineListAPI(ListAPIView):
    model_name = Machine
    serializer_class = MachineListSerializer
    queryset = Machine.objects.filter(status=True)


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
        if not params.get('start'):
            last_seven_days = timezone.now() - timezone.timedelta(days=7)
            queryset = queryset.filter(created_at__gt=last_seven_days)
        else:
            queryset = queryset.filter(Q(created_at__gte=params.get('start')
                                         ) | Q(updated_at__gte=params.get('start')))
        if params.get('end'):
            queryset = queryset.filter(updated_at__lte=params.get('end'))
        if params.get('machine_no'):
            machines = params.get('machine_no').split('-')
            queryset = queryset.filter(machine_no__in=machines)
        if params.get('machine_status'):
            queryset = queryset.filter(machine_status__iexact=params.get('machine_status'))
        return queryset


class MachineDataAnalyticsAPI(APIView):
    model_name = MachineData

    def get(self, request):
        params = request.query_params.dict()
        print("order....", params.get('is_order'), type(params.get('is_order')))

        queryset = MachineData.objects.all()
        if not params.get('start'):
            last_seven_days = timezone.now() - timezone.timedelta(days=7)
            queryset = queryset.filter(created_at__gt=last_seven_days)
        else:
            queryset = queryset.filter(Q(created_at__gte=params.get('start')
                                         ) | Q(updated_at__gte=params.get('start')))
        if params.get('end'):
            queryset = queryset.filter(updated_at__lte=params.get('end'))
        if params.get('machine_no'):
            machines = params.get('machine_no').split('-')
            queryset = queryset.filter(machine_no__in=machines)

        data = queryset.values('machine_no').order_by('machine_no').annotate(
            total_on_time=Sum(Case(When(machine_status='on',
                                        then=F('total_minutes')))),
            total_off_time=Sum(Case(When(machine_status='off',
                                         then=F('total_minutes'))))
        ).annotate(efficiency=(F('total_on_time')*100)/(F('total_on_time')+F('total_off_time')))
        [d.update({'efficiency': 100}) for d in data if not d.get("total_off_time")]

        if params.get("order"):
            if params.get('order').lower() == 'desc':
                data = sorted(data, key=lambda k: k['efficiency'], reverse=True)
            else:
                data = sorted(data, key=lambda k: k['efficiency'], reverse=False)
        return Response(data=data, status=status.HTTP_200_OK)


class MachineDataTotalAnalyticsAPI(APIView):
    model_name = MachineData

    def get(self, request):
        params = request.query_params.dict()
        queryset = MachineData.objects.all()
        start = None
        end = None
        if not params.get('start'):
            last_seven_days = timezone.now() - timezone.timedelta(days=7)
            queryset = queryset.filter(created_at__gte=last_seven_days)
        else:
            queryset = queryset.filter(Q(created_at__gte=params.get('start')
                                         ) | Q(updated_at__gte=params.get('start')))
        if params.get('end'):
            queryset = queryset.filter(updated_at__lte=params.get('end'))
        if params.get('machine_no'):
            machines = params.get('machine_no').split('-')
            queryset = queryset.filter(machine_no__in=machines)
        if queryset:
            start = queryset.order_by('created_at')[0].created_at
            end = queryset.order_by('-updated_at')[0].updated_at
        query = queryset.values('machine_status').order_by('machine_status').aggregate(
            total_on_time=Sum(Case(When(machine_status='on',
                                        then=F('total_minutes')))),
            total_off_time=Sum(Case(When(machine_status='off',
                                         then=F('total_minutes'))))
        )
        on_time = query.get('total_on_time')
        off_time = query.get('total_off_time') or 0
        data = {
            "total_on_time": round(on_time, 2),
            "total_off_time": round(off_time, 2),
            "efficiency": round(on_time*100/(on_time+off_time), 2),
            "start": start,
            "end": end
        }

        return Response(data=data, status=status.HTTP_200_OK)
