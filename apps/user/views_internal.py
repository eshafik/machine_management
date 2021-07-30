from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler, RefreshJSONWebToken

from app_libs.error_codes import ERROR_CODE
from apps.user.models import User


class UserToken(ObtainJSONWebToken):
    """
    A custom class for JWT Token
        URL: /api/v1/user/token/
        Method: POST
    """
    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param format:
        :return:
        :raises
            - KEY_ERROR: mistake spelling username or password
            - NO_CREDENTIALS_PROVIDED: provided empty credential
            - USER_INVALID_CREDENTIALS: provided wrong credential
            - USER_ACCOUNT_BLOCKED: if user blocked
            - USER_ACCOUNT_DEACTIVATED: if user account is deactivated
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user:
                groups = list(user.groups.values_list('name', flat=True))
            else:
                groups = []
            response_data['groups'] = groups
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (timezone.now() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response

        return Response(ERROR_CODE.global_codes.VALUE_ERROR, status=401)


class UserRefreshToken(RefreshJSONWebToken):
    """
    A custom class for JWT Refresh Token
        URL: /api/v1/user/refresh-token/
        Method: POST
    """

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param format:
        :return:
        :raises
            - KEY_ERROR: token keyword is not provided or spelling mistake
            - ALL_FIELDS_REQUIRED: empty token field
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)

            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (timezone.now() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response
        return Response(ERROR_CODE.global_codes.VALUE_ERROR, status=401)
