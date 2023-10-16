import logging
import random
import sys
from datetime import datetime
import decimal
import json
import pytz
import requests
import time
from decimal import Decimal
from dateutil.parser import parse
from dateutil.tz import tzlocal
from django.core.paginator import Paginator
from django.db.models import F
from django.db import transaction
from django.forms import model_to_dict
from django.utils import timezone
from pathlib import Path
from main.settings import BASE_DIR
from xj_enroll.service.enroll_services import EnrollServices
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_payment.utils.join_list import JoinList
from xj_thread.services.thread_list_service import ThreadListService
from xj_user.models import Platform
from xj_user.services.user_platform_service import UserPlatformService
from xj_user.services.user_sso_serve_service import UserSsoServeService
from .payment_alipay_service import PaymentAlipayService
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.custom_tool import format_list_handle, format_params_handle, write_to_log
from ..models import PaymentPayment, PaymentStatus
from ..services.payment_wechat_service import PaymentWechatService
from ..utils.utility_method import find, format_dates

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

# 小程序appid
sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""
# 服务号appid
subscription_app_id = main_config_dict.wechat_subscription_app_id or module_config_dict.wechat_subscription_app_id or ""
# 商户名称
merchant_name = main_config_dict.merchant_name or module_config_dict.merchant_name or ""


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, int):
                return int(obj)
            elif isinstance(obj, float) or isinstance(obj, decimal.Decimal):
                return float(obj)
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, time) or isinstance(obj, datetime.timedelta):
                return obj.__str__()
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            # logger.exception(e, stack_info=True)
            return obj.__str__()


class PaymentLogicalProcessService:
    # 支付逻辑处理
    @staticmethod
    @transaction.atomic
    def payment_logic_processing(param, pay_mode="WECHAT"):
        sid = transaction.savepoint()
        try:
            out_trade_no = param['out_trade_no']  # 订单号
            total_fee = param['total_fee']  # 金额（单位分）
            total_amount = int(total_fee) / 100  # 分转元
            # if pay_mode != "WECHAT":
            #     total_amount = total_fee
            transact_no = 0
            if 'transaction_id' in param:
                transact_no = param['transaction_id']  # 支付订单号
            data = {
                "order_no": out_trade_no,
                "amount": total_amount,
                "pay_mode": pay_mode
            }
            # 根据订单号查询支付记录是否存在
            payment = PaymentPayment.objects.filter(order_no=int(out_trade_no)).first()
            if not payment:
                write_to_log(
                    prefix="out_trade_no" + str(out_trade_no) + "支付记录不存在",
                )
            payment_message = model_to_dict(payment)
            data['account_id'] = payment_message['user_id']
            data['enroll_id'] = payment_message['enroll_id']
            goods_info = {}
            data['goods_info'] = goods_info
            # # TODO 拿到订单号后的操作 看自己的业务需求
            # 写入资金模块
            finance, err_txt = FinanceTransactService.finance_flow_writing(params=data, finance_type='TOP_UP')
            if err_txt:
                write_to_log(
                    prefix=str(data) + "写入资金模块失败",
                    content=err_txt
                )
            # 根据唯一交易id 查询主键id
            payment_status_set = PaymentStatus.objects.filter(payment_status="成功").first()
            payment_data = {
                "transact_no": transact_no,
                "payment_time": param.get("payment_time", None) if param.get("payment_time", None) else None,
                "payment_status": payment_status_set.id,
                "pay_mode": pay_mode,
                "order_status_id": 2,

            }
            # 更改支付记录
            PaymentPayment.objects.filter(order_no=int(out_trade_no)).update(**payment_data)
            # 报名表支付状态修改
            pay_call_back_data, pay_call_back_err = EnrollServices.bxtx_pay_call_back(out_trade_no)
            if pay_call_back_err:
                write_to_log(
                    prefix="报名表支付状态修改",
                    content="out_trade_no:" + str(out_trade_no),
                    err_obj=pay_call_back_err
                )

        except Exception as err:
            write_to_log(
                prefix="支付回调异常",
                content="",
                err_obj=err
            )
            transaction.savepoint_rollback(sid)
