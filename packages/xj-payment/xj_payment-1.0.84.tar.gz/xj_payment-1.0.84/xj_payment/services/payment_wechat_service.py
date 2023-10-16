import decimal
import json
import logging
import os
import sys
from pathlib import Path
from random import sample
from string import ascii_letters, digits
import time
import datetime

from django.db import transaction
from django.forms import model_to_dict
from lxml import etree as et
import requests
from wechatpayv3 import WeChatPayType

from main.settings import BASE_DIR
from xj_enroll.service.enroll_services import EnrollServices
from xj_finance.services.finance_service import FinanceService
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_user.services.user_sso_serve_service import UserSsoServeService
from ..models import PaymentStatus
from ..utils.custom_tool import write_to_log
from ..models import PaymentPayment
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.wechat_utils import my_ali_pay, my_ali_pay_v3, to_text, random_string, applets_red_envelopes
from logging import getLogger

logger = getLogger('log')

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
# APPID，应用ID或服务商模式下的sp_appid
app_id = main_config_dict.wechat_service_app_id or module_config_dict.wechat_service_app_id or ""
# 商户号（服务号）
mch_id = main_config_dict.wechat_service_mch_id or module_config_dict.wechat_service_mch_id or ""
# 小程序SECRET （服务号）
app_secret = main_config_dict.wechat_service_app_secret or module_config_dict.wechat_service_app_secret or ""
# 商户KEY（服务号）
merchant_key = main_config_dict.wechat_service_merchant_key or module_config_dict.wechat_service_merchant_key or ""
# 小程序ID（子商户）
sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""
# 小程序SECRET （子商户）
sub_app_secret = main_config_dict.wechat_merchant_app_secret or module_config_dict.wechat_merchant_app_secret or ""
# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
sub_mch_id = main_config_dict.wechat_merchant_mch_id or module_config_dict.wechat_merchant_mch_id or ""
# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
apiv3_secret = main_config_dict.wechat_apiv3_secret or module_config_dict.wechat_apiv3_secret or ""

subscription_app_id = main_config_dict.wechat_subscription_app_id or module_config_dict.wechat_subscription_app_id or ""

app_app_id = main_config_dict.wechat_app_app_id or module_config_dict.wechat_app_app_id or ""
# 商户证书序列号
cert_serial_no = main_config_dict.wechat_cert_serial_no or module_config_dict.wechat_cert_serial_no or ""
# 微信支付平台证书缓存目录，减少证书下载调用次数
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
cert_dir = main_config_dict.wechat_cert_dir or module_config_dict.wechat_cert_dir or ""
# 商品描述，商品简单描述
description = main_config_dict.wechat_body or module_config_dict.wechat_body or ""
# 标价金额，订单总金额，单位为分
total_fee = main_config_dict.wechat_total_fee or module_config_dict.wechat_total_fee or ""
# 通知地址，异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。回调地址，也可以在调用接口的时候覆盖
notify_url = main_config_dict.wechat_notify_url or module_config_dict.wechat_notify_url or ""
# 新版回调地址
notify_url_v3 = main_config_dict.wechat_notify_url_v3 or module_config_dict.wechat_notify_url_v3 or ""
# 商户名称
merchant_name = main_config_dict.merchant_name or module_config_dict.merchant_name or ""
# 商户证书私钥路径
private_key_path = main_config_dict.wechat_merchant_private_key_file or module_config_dict.wechat_merchant_private_key_file or (
        str(BASE_DIR) + "/config/cert/apiclient_key.pem")

# 读取文件获取密钥
private_key = open(private_key_path, encoding="utf-8").read() if os.path.exists(private_key_path) else ""
# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")
# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = True
# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None
url = "https://api.mch.weixin.qq.com/v3/pay/partner/transactions/jsapi"
logger = logging.getLogger(__name__)


class Networkerror(Exception):
    def __init__(self, arg):
        self.args = arg


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


class PaymentWechatService:
    # 微信支付
    @staticmethod
    def wechat_jsapi(params, payment_type=None):
        """统一下单
           :return code, message:
           :param description: 商品描述，示例值:'Image形象店-深圳腾大-QQ公仔'
           :param out_trade_no: 商户订单号，示例值:'1217752501201407033233368018'
           :param amount: 订单金额，示例值:{'total':100, 'currency':'CNY'}
           :param payer: 支付者，示例值:{'openid':'oHkLxtx0vUqe-18p_AXTZ1innxkCY'}
           :param time_expire: 交易结束时间，示例值:'2018-06-08T10:34:56+08:00'
           :param attach: 附加数据，示例值:'自定义数据'
           :param goods_tag: 订单优惠标记，示例值:'WXG'
           :param detail: 优惠功能，示例值:{'cost_price':608800, 'invoice_id':'微信123', 'goods_detail':[{'merchant_goods_id':'商品编码', 'wechatpay_goods_id':'1001', 'goods_name':'iPhoneX 256G', 'quantity':1, 'unit_price':828800}]}
           :param scene_info: 场景信息，示例值:{'payer_client_ip':'14.23.150.211', 'device_id':'013467007045764', 'store_info':{'id':'0001', 'name':'腾讯大厦分店', 'area_code':'440305', 'address':'广东省深圳市南山区科技中一道10000号'}}
           :param settle_info: 结算信息，示例值:{'profit_sharing':False}
           :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
           :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
           :param mchid: 微信支付商户号，可不填，默认传入初始化的mchid，示例值:'987654321'
           :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
           :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
           :param support_fapiao: 电子发票入口开放标识，传入true时，支付成功消息和支付详情页将出现开票入口。
           :param pay_type: 微信支付类型，示例值:WeChatPayType.JSAPI
        """
        wxpay = my_ali_pay_v3()
        sso = {}
        if payment_type == "applets":
            app_id = sub_appid
        elif payment_type == "wechat_web":
            app_id = subscription_app_id
        elif payment_type == "wechat_app":
            wxpay = my_ali_pay_v3(wechatpay_type=WeChatPayType.APP)
            app_id = app_app_id
        if payment_type in ["applets", "wechat_web"]:
            sso, err = UserSsoServeService.user_sso_to_user(params['user_id'], app_id)
            if err and payment_type != "wechat_app":
                return None, {"error": "60005", "msg": "未授权登录1"}
            if not sso['sso_unicode'] and payment_type != "wechat_app":
                return None, {"error": "60005", "msg": "未授权登录2"}
        try:
            if payment_type in ["applets", "wechat_web"]:
                code, message = wxpay.pay(
                    description=description,
                    out_trade_no=params['out_trade_no'],
                    sub_appid=app_id,
                    sub_mchid=sub_mch_id,
                    notify_url=notify_url_v3,
                    amount={'total': int(params['total_fee'])},
                    payer={'sub_openid': sso.get("sso_unicode", "")}
                )
            else:
                code, message = wxpay.pay(
                    description=description,
                    out_trade_no=params['out_trade_no'],
                    sub_appid=app_id,
                    sub_mchid=sub_mch_id,
                    notify_url=notify_url_v3,
                    amount={'total': int(params['total_fee'])})

            result = json.loads(message)
            if code in range(200, 300):
                prepay_id = result.get('prepay_id')
                timestamp = to_text(int(time.time()))
                noncestr = random_string(32)
                if payment_type == "wechat_app":
                    paysign = wxpay.sign([app_id, timestamp, noncestr, prepay_id])
                else:
                    package = 'prepay_id=' + prepay_id
                    paysign = wxpay.sign([app_id, timestamp, noncestr, package])
                signtype = 'RSA'
            else:
                return None, {"error": "47767", "msg": str(result)}
        except Exception as e:
            return None, {"error": "47767", "msg": str(e)}
        data = {
            'appId': app_id,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'partnerid': sub_mch_id,
            'prepay_id': prepay_id,
            'signType': signtype,
            'paySign': paysign
        }
        if payment_type == "wechat_app":
            data['package'] = "Sign=WXPay"
        else:
            data['package'] = 'prepay_id=%s' % prepay_id
        return data, None

    # 微信退款
    @staticmethod
    def payment_refund(params):
        """申请退款
            :param out_refund_no: 商户退款单号，示例值:'1217752501201407033233368018'
            :param amount: 金额信息，示例值:{'refund':888, 'total':888, 'currency':'CNY', 'refund_fee':100}
            :param transaction_id: 微信支付订单号，示例值:'1217752501201407033233368018'
            :param out_trade_no: 商户订单号，示例值:'1217752501201407033233368018'
            :param reason: 退款原因，示例值:'商品已售完'
            :param funds_account: 退款资金来源，示例值:'AVAILABLE'
            :param goods_detail: 退款商品，示例值:{'merchant_goods_id':'1217752501201407033233368018', 'wechatpay_goods_id':'1001', 'goods_name':'iPhone6s 16G', 'unit_price':528800, 'refund_amount':528800, 'refund_quantity':1}
            :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
            :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
        """
        wxpay = my_ali_pay_v3()
        out_refund_no = ''.join(sample(ascii_letters + digits, 8))
        code, message = wxpay.refund(
            out_refund_no=out_refund_no,
            amount={'refund': int(params['refund_fee']), 'total': int(params['refund_fee']), 'currency': 'CNY'},
            transaction_id=params['transaction_id'],
            notify_url=notify_url_v3,
            sub_mchid=sub_mch_id,
        )
        result = json.loads(message)
        return result

    # 支付回调（老版）
    @staticmethod
    def callback_old(body):
        """
        <xml><appid><![CDATA[wx56232dd67c7e5a18]]></appid> 微信分配的小程序ID
        <bank_type><![CDATA[CFT]]></bank_type>付款银行
        <cash_fee><![CDATA[1]]></cash_fee>现金支付金额订单现金支付金额
        <fee_type><![CDATA[CNY]]></fee_type>货币类型
        <is_subscribe><![CDATA[N]]></is_subscribe>用户是否关注公众账号，Y-关注，N-未关注
        <mch_id><![CDATA[1521497251]]></mch_id>微信支付分配的商户号
        <nonce_str><![CDATA[1546088296922]]></nonce_str>随机字符串，不长于32位
        <openid><![CDATA[oEHJT1opJZLYBWssRlyjq9bSdnao]]></openid>用户在商户appid下的唯一标识
        <out_trade_no><![CDATA[10657298351779092719122609746693]]></out_trade_no>商户系统内部订单号，要求32个字符内
        <result_code><![CDATA[SUCCESS]]></result_code>业务结果 SUCCESS/FAIL
        <return_code><![CDATA[SUCCESS]]></return_code>返回状态码 return_code
        <sign><![CDATA[2EB71F6237E04C3DA4B1509A502E8F62]]></sign>签名
        <time_end><![CDATA[20181229205830]]></time_end>支付完成时间
        <total_fee>1</total_fee>订单总金额，单位为分
        <trade_type><![CDATA[MWEB]]></trade_type>交易类型 JSAPI、NATIVE、APP
        <transaction_id><![CDATA[4200000224201812291041578058]]></transaction_id>微信支付订单号
        </xml>
        """

        # _xml = request.body
        # 拿到微信发送的xml请求 即微信支付后的回调内容
        xml = str(body, encoding="utf-8")
        return_dict = {}
        tree = et.fromstring(xml)
        # xml 解析
        return_code = tree.find("return_code").text
        try:
            if return_code == 'FAIL':
                # 官方发出错误
                return_dict['return_code'] = "SUCCESS"
                return_dict['return_msg'] = "OK"
                logging.error("微信支付失败")
                # return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
            elif return_code == 'SUCCESS':
                # 拿到自己这次支付的 out_trade_no
                out_trade_no = tree.find("out_trade_no").text  # 订单号
                total_fee = tree.find("total_fee").text  # 金额（单位分）
                transaction_id = tree.find("transaction_id").text  # 微信支付订单号
                appid = tree.find("appid").text  #
                param = {
                    "out_trade_no": out_trade_no,
                    "total_fee": total_fee,
                    "transaction_id": transaction_id,
                    "appid": appid
                }
                PaymentWechatService.payment_logic_processing(param)
                return_dict['return_code'] = "SUCCESS"
                return_dict['return_msg'] = "OK"
        except Exception as e:
            return_dict['message'] = str(e)
        finally:
            xml_data = "<xml><return_code><![CDATA[{return_code}]]></return_code><return_msg><![CDATA[{return_msg}]]></return_msg> </xml> "
            kw = {'return_code': 'SUCCESS', 'return_msg': 'OK'}
            # 格式化字符串
            xml = xml_data.format(**kw)
            return xml
            # 小程序回调

    # 支付回调（新版）
    @staticmethod
    def callback(headers, body):
        wxpay = my_ali_pay_v3()
        result = wxpay.callback(headers=headers, body=body)
        if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
            resource = result.get('resource')
            sp_appid = resource.get('sp_appid')  # 服务商应用ID	sp_appid
            sp_mchid = resource.get('sp_mchid')  # 服务商户号	sp_mchid
            sub_appid = resource.get('sub_appid')  # 子商户应用ID	sub_appid
            sub_mchid = resource.get('sub_mchid')  # 子商户号	sub_mchid
            out_trade_no = resource.get('out_trade_no')  # 商户订单号	out_trade_no
            transaction_id = resource.get('transaction_id')  # 微信支付订单号	transaction_id
            trade_type = resource.get('trade_type')  # 交易类型	trade_type
            trade_state = resource.get('trade_state')  # 交易状态	trade_state
            trade_state_desc = resource.get('trade_state_desc')  # 交易状态描述	trade_state_desc
            bank_type = resource.get('bank_type')  # 付款银行	bank_type
            attach = resource.get('attach')  # 附加数据	attach
            success_time = resource.get('success_time')  # 支付完成时间	success_time
            payer = resource.get('payer')  # 支付者信息
            amount = resource.get('amount').get('total')  # 订单金额
            # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
            param = {
                "out_trade_no": out_trade_no,
                "total_fee": amount,
                "transaction_id": transaction_id,
                "appid": sub_appid,
                "payment_time": success_time,
                "pay_mode": 2
            }
            if not sys.modules.get("xj_payment.services.payment_logical_process_service.PaymentLogicalProcessService"):
                from xj_payment.services.payment_logical_process_service import PaymentLogicalProcessService
                PaymentLogicalProcessService.payment_logic_processing(param=param)
            return {'code': 'SUCCESS', 'message': '成功'}
        if result and result.get('event_type') == 'REFUND.SUCCESS':
            resource = result.get('resource')
            sp_mchid = resource.get('sp_mchid')  # 服务商户号	sp_mchid
            sub_mchid = resource.get('sub_mchid')  # 子商户号	sub_mchid
            out_trade_no = resource.get('out_trade_no')  # 商户订单号	out_trade_no
            transaction_id = resource.get('transaction_id')  # 微信支付订单号	transaction_id
            out_refund_no = resource.get('out_refund_no')  # 商户退款单号	out_refund_no
            refund_id = resource.get('refund_id')  # 微信支付退款单号	refund_id
            refund_status = resource.get('refund_status')  # 退款状态	refund_status
            success_time = resource.get('success_time')  # 退款成功时间	success_time
            user_received_account = resource.get('user_received_account')  # 退款入账账户
            amount = resource.get('amount').get('refund')  # 退款金额
        else:
            resource = result.get('resource')
            out_trade_no = resource.get('out_trade_no')
            payment_status_set = PaymentStatus.objects.filter(payment_status="失败").first()
            payment_data = {
                "payment_status_id": payment_status_set.id
            }
            PaymentPayment.objects.filter(order_no=int(out_trade_no)).update(**payment_data)
            return {'code': 'FAILED', 'message': '失败'}
