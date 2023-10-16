from django.core.paginator import Paginator
from django.db.models import F
from xj_payment.models import PaymentStatus


class PaymentStatusService:
    @staticmethod
    def list(params):
        size = params.pop('size', 20)
        page = params.pop('page', 20)
        list_obj = PaymentStatus.objects.filter(**params).order_by('-id')
        count = list_obj.count()
        list_obj = list_obj.values(
            "id",
            "payment_status",
            "group",
            "description",
        )
        res_set = Paginator(list_obj, size).get_page(page)
        page_list = []
        if res_set:
            page_list = list(res_set.object_list)

        return {'total': count, 'page': page, 'size': size, "list": page_list}, None

    @staticmethod
    def add(params):
        try:
            PaymentStatus.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

