from django.http import JsonResponse
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_libs.success_codes import SUCCESS_CODE
from app_libs.error_codes import ERROR_CODE
from apps.user.models import User
from apps.user.validations import x_data_validation


# custom json response for page not found
def error404(request, exception):
    return JsonResponse({"Message": "Page not found", "code": "PNF404"}, status=404)
