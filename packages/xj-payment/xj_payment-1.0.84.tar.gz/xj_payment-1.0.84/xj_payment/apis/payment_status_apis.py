from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_common.utils.custom_tool import request_params_wrapper
from xj_common.utils.user_wrapper import user_authentication_wrapper
from xj_payment.services.payment_satus_service import PaymentStatusService
from xj_payment.services.payment_service import PaymentService
from xj_user.services.user_service import UserService
from ..utils.model_handle import parse_data, util_response


class PaymentStatusApis(APIView):

    # 支付状态列表
    @require_http_methods(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        data, err_txt = PaymentStatusService.list(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)

    # 支付列表添加
    @require_http_methods(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        data, err_txt = PaymentStatusService.add(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)
