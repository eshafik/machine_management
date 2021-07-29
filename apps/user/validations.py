from django.contrib.auth import authenticate

from app_libs import exceptions
from app_libs.error_codes import ERROR_CODE
from app_libs.validators import is_phone_valid, is_sol_email_valid


def x_data_validation(func):
    """
    A simple data validation decorator
    :param func:
    :return:
    :raises:
        - if X is not valid key: KEY_ERROR
        - if X is not valid format: VALUE_ERROR
    """
    keys = ["username"]

    def validation(request, *args, **kwargs):
        if all(key in request.data.keys() for key in keys):
            if not is_phone_valid(request.data.get('username')) and not is_sol_email_valid(
                    request.data.get('username')):
                raise exceptions.ValidationError(ERROR_CODE.global_codes.VALUE_ERROR)
        else:
            raise exceptions.ValidationError(ERROR_CODE.global_codes.KEY_ERROR)
        return func(request, *args, **kwargs)

    return validation
