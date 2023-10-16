from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from xj_enroll.service.enroll_services import EnrollServices
from xj_thread.services.thread_list_service import ThreadListService
from ..utils.custom_tool import request_params_wrapper, format_params_handle, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_wrapper
from ..services.payment_service import PaymentService
from ..utils.model_handle import parse_data, util_response
from ..utils.utility_method import extract_values


class PaymentApis(APIView):

    # 支付列表
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("user_id", user_id)  # 用户ID
        params.setdefault("platform_id", platform_id)  # 平台
        # ================== 信息id列表反查询报名 start===============================
        thread_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["title", "subtitle", "access_level", "author"],
            is_remove_empty=True
        )
        if thread_params:
            thread_ids, err = ThreadListService.search_ids(search_prams=thread_params)
            if not err:
                request_params["thread_id_list"] = thread_ids

            # TODO 镖行的逻辑和其他逻辑不一样
            if isinstance(request_params.get("thread_id_list"), list) and len(
                    request_params["thread_id_list"]) == 0:
                request_params["thread_id_list"] = [0]
            if request_params.get("is_bx", None):
                enroll_list, err = EnrollServices.enroll_list({"thread_id_list": request_params["thread_id_list"]})
                if not err:
                    request_params["enroll_id_list"] = extract_values(enroll_list['list'], 'id')
                    if isinstance(request_params.get("enroll_id_list"), list) and len(
                            request_params["enroll_id_list"]) == 0:
                        request_params["enroll_id_list"] = [0]

                    request_params.pop("thread_id_list")
        # ================== 信息id列表反查询报名 end ===============================
        data, err_txt = PaymentService.list(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)

    # 支付总接口
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def pay(self, *args, user_info, request_params, **kwargs, ):
        response = HttpResponse()
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("user_id", user_id)  # 用户ID
        params.setdefault("platform_id", platform_id)  # 平台
        data, err_txt = PaymentService.pay(params)
        if err_txt:
            if isinstance(err_txt, dict) and err_txt.get("error"):
                content = util_response(err=int(err_txt['error']), msg=err_txt['msg'])
            else:
                content = util_response(err=47767, msg=err_txt)
        else:
            content = util_response(data=data)
        response.content = content
        return response

    @api_view(['GET'])
    @request_params_wrapper
    def ask_order_status(self, *args, request_params, **kwargs, ):
        params = request_params
        data, err_txt = PaymentService.ask_order_status(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)

    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def golden_touch(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        data, err_txt = PaymentService.golden_touch(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)

    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def golden_touch(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        data, err_txt = PaymentService.golden_touch(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)

    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def refund(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        data, err_txt = PaymentService.refund(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return util_response(data=data)