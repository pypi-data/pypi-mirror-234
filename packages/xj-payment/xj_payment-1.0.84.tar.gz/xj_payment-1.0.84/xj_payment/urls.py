# 应用名称
from django.urls import re_path

from xj_payment.apis import alipay, transaction_inquiry, payment, payment_status
from xj_payment.apis.payment_apis import PaymentApis
from xj_payment.apis.payment_status_apis import PaymentStatusApis
from .apis import payment_alipay
from .apis import payment_wechat
from .apis import payment_unionpay
from .apis import payment

app_name = 'payment'

urlpatterns = [
    re_path(r'^get_pay_url/?$', payment_alipay.PaymentAlipay.get_pay_url),  # 获取支付宝支付链接
    re_path(r'^get_result/?$', payment_alipay.PaymentAlipay.pay_result),  # 支付宝处理完成后同步回调通知
    re_path(r'^update_order/?$',payment_alipay.PaymentAlipay.update_order),  # 支付宝处理完成后支付宝服务器异步回调通知
    re_path(r'^close/?$', alipay.Payment.close),  # 关闭订单

    re_path(r'^refund_inquiry/?$', transaction_inquiry.query.refund_inquiry),  # 支付宝退款查询
    re_path(r'^trade_query/?$', transaction_inquiry.query.trade_query),  # 支付宝下单查询

    re_path(r'^get_user_info/?$', payment_wechat.PaymentWechat.get_user_info),  # 获取用户标识接口
    re_path(r'^scan_pay/?$', payment_wechat.PaymentWechat.payment_scan_pay),  # 微信扫码支付
    re_path(r'^red_envelopes/?$', payment_wechat.PaymentWechat.payment_red_envelopes),  # 微信红包
    re_path(r'^wechat_callback/?$', payment_wechat.PaymentWechat.callback, name="微信回调接口"),  # 微信回调接口
    re_path(r'^wechat_callback_v3/?$', payment_wechat.PaymentWechat.callback_v3, name="微信回调接口（新）"),  # 微信回调接口
    re_path(r'^logic/?$', payment_wechat.PaymentWechat.logic),  # 支付逻辑处理模拟

    re_path(r'^unipay/?$', payment_unionpay.PaymentUnionPay.unipay),

    re_path(r'^refund/?$', payment.Payment.refund, name="退款总接口"),

    re_path(r'^pay/?$', PaymentApis.pay, name="支付总接接口"),  # 支付总接接口
    re_path(r'^list/?$', PaymentApis.list, name="支付列表"),
    re_path(r'^ask_order_status/?$', PaymentApis.ask_order_status),
    re_path(r'^golden_touch/?$', PaymentApis.golden_touch),

    re_path(r'^status_add/?$', PaymentStatusApis.add, name="支付状态添加"),  # 支付状态添加
    re_path(r'^status_list/?$', PaymentStatusApis.list, name="支付状态列表"),  # 支付状态列表
]
