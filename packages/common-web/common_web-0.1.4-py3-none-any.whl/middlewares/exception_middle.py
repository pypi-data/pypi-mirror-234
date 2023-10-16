import sys
import traceback

from django.utils.deprecation import MiddlewareMixin

from dto.res_dto import ResObj
from exception.auth_exception import AuthException
from exception.business_exception import BusinessException

SYSTEM_EXCEPTION_CODE = 999
BUSINESS_EXCEPTION_CODE = 500
AUTH_EXCEPTION_CODE = 400


class ExceptionMiddle(MiddlewareMixin):
    """
    全局拦截异常信息 For Django
    """

    def process_exception(self, request, exception):
        print('exception is:', exception)
        traceback.print_exc()
        if isinstance(exception, BusinessException):
            code = BUSINESS_EXCEPTION_CODE
            message = exception.value
        elif isinstance(exception, AuthException):
            code = AUTH_EXCEPTION_CODE
            message = exception.value
        else:
            code = SYSTEM_EXCEPTION_CODE
            message = "system error"
        return ResObj(code=code, message=message).json()
