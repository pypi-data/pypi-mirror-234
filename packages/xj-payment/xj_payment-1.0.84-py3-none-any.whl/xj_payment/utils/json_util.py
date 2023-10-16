import decimal
import json
from datetime import time, datetime, date, timedelta


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, int):
                return int(obj)
            elif isinstance(obj, float) or isinstance(obj, decimal.Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, time) or isinstance(obj, timedelta):
                return obj.__str__()
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            # logger.exception(e, stack_info=True)
            return obj.__str__()


# def json_encode(val_obj):
#     """
#     对象转JSON字符串
#     :param val_obj: 值对象
#     :return:
#     """
#     return json.dumps(val_obj, cls=MyEncoder, ensure_ascii=False)
#
#
# def json_decode(json_str, default=None):
#     """
#     JSON字符串转对象
#     :param json_str: JSON字符串
#     :param default: 默认值，比如：{} 或 []
#     :return:
#     """
#     if default is None:
#         default = {}
#     if string_is_empty(json_str):
#         return default
#     return json.loads(json_str)