# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 返回协议封装工具
@created_time: 2022/6/15 14:14
"""
import datetime
import decimal
import json
import traceback
import uuid

from django.http import JsonResponse
from django.utils.duration import duration_iso_string
from django.utils.functional import Promise
from django.utils.timezone import is_aware

from .custom_tool import write_to_log


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal)):
            return float(o)

        elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        else:
            return super().default(o)


# json 结果集返回
def parse_json_str(result):
    if not result is None:
        if type(result) is str:
            try:
                json_result = json.loads(
                    result.replace("'", '"').replace('\\r', "").replace('\\n', "").replace('\\t', "").replace('\\t', "").replace("None", "null").replace("False", 'false').replace("True", 'true')
                )
                # json.loads, 会把默认的数字格式的字符串转换为int类型,所以这里不希望强制转换所以，再次转换回来
                result = result if isinstance(json_result, int) else json_result
            except Exception as e:
                return result
        if type(result) is list or type(result) is tuple:
            for index, value in enumerate(result):
                result[index] = parse_json_str(value)
        if type(result) is dict:
            for k, v in result.items():
                result[k] = parse_json_str(v)
    return result


# 数据返回规则
def util_response(data='', err=0, msg='ok', is_need_parse_json=True, cookies=None):
    """
    http 返回协议封装
    :param is_need_parse_json: 是否需要解析json字符串
    :param cookies: 设置cookie的json
    :param data: 返回的数据体
    :param err: 错误码，一般以1000开始，逐一增加。登录错误为6000-6999。
    :param msg: 错误信息，一般为服务返回协议中的err,自动解析内容
    :return: response对象
    """
    # ============= section 构建body的json数据 start =================
    data = parse_json_str(data) if is_need_parse_json else data
    response_json = {'err': err, 'data': data}
    # 解析msg字符串
    try:
        msg_list = msg.split(";")
        if len(msg_list) <= 1:
            response_json["msg"] = msg
        else:
            for i in msg_list:
                [key, value] = i.split(":")
                response_json[key] = value
    except Exception as e:
        # 获取谁调用该函数
        try:
            call_file_obj = traceback.extract_stack()[-2]
            call_file_name = str(call_file_obj.filename)
            call_file_line = str(call_file_obj.lineno)
        except Exception as get_call_file_err:
            call_file_name = ""
            call_file_line = ""
        # 写入日志
        write_to_log(
            prefix="返回消息异常，请提前处理好份号‘：’，请及时修改",
            content="msg:" + str(msg) + "调用文件：" + call_file_name + "  行数：" + call_file_line
        )
        response_json["msg"] = msg
    # ============= section 构建body的json数据 end =================

    # ============= section 构建响应对象 start =================
    response = JsonResponse(response_json, encoder=CustomJSONEncoder)
    # 设置cookie
    if cookies and isinstance(cookies, dict):
        for k, v in cookies.items():
            response.set_cookie(k, value=v)
    # ============= section 构建响应对象 end =================
    return response
