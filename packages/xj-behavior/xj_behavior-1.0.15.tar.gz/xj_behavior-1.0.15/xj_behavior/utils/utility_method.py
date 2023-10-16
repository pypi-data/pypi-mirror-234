"""
Created on 2023-07-20
@author:高栋天
@description:自定义方法
"""
import pinyin
import uuid
import json
import sys
import time
import os
import string
import random
import pytz
import datetime
from django.utils import timezone
from dateutil.parser import parse
from dateutil.tz import tzlocal
import pandas as pd
from datetime import datetime
from decimal import Decimal


# 获取当前时间
def get_current_time():
    # TODO USE_TZ = False 时会报错 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
    tz = pytz.timezone('Asia/Shanghai')
    # 返回datetime格式的时间
    now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S.%f")
    # now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.now().strptime(now_time, "%Y-%m-%d %H:%M:%S.%f")
    return now


def get_current_time_second():
    # 设置时区为Asia/Shanghai
    tz = pytz.timezone('Asia/Shanghai')

    # 获取当前的UTC时间
    utc_now = datetime.now(pytz.utc)

    # 将UTC时间转换为您指定的时区（Asia/Shanghai）并转换为字符串格式
    now_time = utc_now.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

    # 返回当前时间的字符串格式
    return now_time


# 时间精确到微秒
def append_microsecond_to_datetime(datetime_str: str) -> datetime:
    """
    将当前微秒追加到日期时间字符串中。如果字符串仅包含日期，当前时间也附加在微秒之前。
    """
    # Check if the datetime string contains a time
    if len(datetime_str.split(' ')) == 2:
        current_microsecond = datetime.now().strftime("%f")
        datetime_str = f'{datetime_str}.{current_microsecond}'
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    else:
        # Get the current time and microsecond
        current_time_microsecond = datetime.now().strftime("%H:%M:%S.%f")
        datetime_str = f'{datetime_str} {current_time_microsecond}'
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    return dt


# 数据key替换
def replace_dict_key(dictionary, old_key, new_key):
    """
       :param dictionary: 字典
       :param old_key: 旧key
       :param new_key: 替换的新key
   """
    if old_key in dictionary:
        dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


# 数据字典key替换
def replace_key_in_dict(original_dict, old_key, new_key):
    """
       :param original_dict: 字典
       :param old_key: 旧key
       :param new_key: 替换的新key
   """
    copied_dict = original_dict.copy()
    if old_key in copied_dict:
        copied_dict[new_key] = copied_dict.pop(old_key)
    return copied_dict


# 数据列表key替换
def replace_key_in_list_dicts(list_dicts, old_keys, new_key):
    """
       :param list_dicts: 列表
       :param old_key: 旧key
       :param new_key: 替换的新key
    """
    for d in list_dicts:
        for old_key in old_keys:
            if old_key in d:
                d[new_key] = d.pop(old_key)
    return list_dicts


# 字典替换字典
def replace_key_in_dict_replacement_dicts(dict_data, replacement_dict):
    """
      :param dict_data: 字典
      :param replacement_dict: 替换的字典映射
   """
    for old_key, new_key in replacement_dict.items():
        if old_key in dict_data:
            dict_data[new_key] = dict_data.pop(old_key, dict_data[old_key])
    return dict_data


# 数据列表字典key替换
def replace_key_in_list_replacement_dicts(list_dicts, replacement_dict):
    """
       :param list_dicts: 列表
       :param replacement_dict: 要替换的字典
    """
    for d in list_dicts:
        for old_key, new_key in replacement_dict.items():
            if old_key in d:
                d[new_key] = d.pop(old_key)
    return list_dicts


# 字符串转列表
# 1. 如果传入的是字符串，它会检查是否有逗号，然后将其分割成列表或者直接转为包含一个元素的列表。
# 2. 如果传入的是整数，它会将整数转换成字符串，并放入一个列表中。
# 3. 如果传入的是列表，它会将列表中的每个元素转换成字符串。
def parse_integers(value):
    if isinstance(value, str):
        if "," in value:
            lst = value.split(",")
        else:
            lst = [value]
    elif isinstance(value, int):
        lst = [str(value)]
    elif isinstance(value, list):
        lst = [str(num) for num in value]
    else:
        raise ValueError("不支持的值类型。应为字符串、int或list")

    return lst


# 保留两位小数
def keep_two_decimal_places(str_num):
    """
    :param str_num: 要处理的字段
    """
    result_num = format(float(str_num), "")

    if len(result_num.split(".")[-1]) < 2:
        result_num = result_num + "0"
    return result_num


# 生成一个长度为16的密码
def generate_password(length=16):
    """
     :param length: 长度
     """
    # 合并所有可能的字符，包括大小写字母、数字和标点符号
    # all_chars = string.ascii_letters + string.digits + string.punctuation
    all_chars = string.ascii_letters + string.digits
    # length = random.randint(8, 12)
    # 随机选择指定数量的字符
    password = ''.join(random.choice(all_chars) for _ in range(length))

    return password


# 数字表示生成几位, True表示生成带有字母的 False不带字母的
def get_code(n=6, alpha=False):
    """
     :param n: 要生成的位数
     :param alpha: True表示生成带有字母的 False不带字母的
     """
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(1, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


# 检查列表字段是否存在
def find(list, keyword):
    """
   :param list: 列表
   :param keyword: 要检查的字段
   """
    try:
        list.index(keyword)
        return True
    except ValueError:
        return False


# 批量数据时间格式化
def format_dates(data, date_fields):
    """
   :param data: 列表
   :param date_fields: 要格式化的字段列表
   """
    for item in data:
        for field in date_fields:
            if field in item and item[field]:
                try:
                    # 如果字段已经是 datetime 对象，就无需解析
                    if isinstance(item[field], datetime):
                        date = item[field]
                    else:
                        # 尝试解析并格式化日期
                        date = parse(item[field])
                    # 使用 strftime 格式化日期
                    item[field] = date.astimezone(tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # 如果解析失败，保留原来的值
                    pass
    return data


# 列表根据指定key计算value求和
# def aggregate_data(data_list, group_field, agg_fields):
#     """
#    :param data_list: 列表
#    :param group_field: 分组规则
#    :param agg_fields: 要求和的字段
#    """
#     # 将数据转换为 DataFrame
#     df = pd.DataFrame(data_list)
#
#     # 将累加字段转换为数值型
#     for field in agg_fields:
#         df[field] = pd.to_numeric(df[field])
#
#     # 根据 group_field 对数据进行分组，并对 agg_fields 进行求和
#     grouped = df.groupby(group_field)[agg_fields].sum().reset_index()
#
#     # 将结果转换回字典列表
#     grouped_data = grouped.to_dict('records')
#
#     return grouped_data

# def aggregate_data(data_list, group_field, agg_fields):
#     """
#     :param data_list: 列表
#     :param group_field: 分组规则
#     :param agg_fields: 要求和的字段列表
#     """
#     # 将数据转换为 DataFrame
#     df = pd.DataFrame(data_list)
#
#     # 将累加字段转换为数值型
#     for field in agg_fields:
#         df[field] = pd.to_numeric(df[field], errors='coerce')  # 处理可能的NaN值
#
#     # 将NaN值替换为0
#     df.fillna(0, inplace=True)
#
#     # 根据 group_field 对数据进行分组，并对 agg_fields 进行求和
#     grouped = df.groupby(group_field)[agg_fields].sum().reset_index()
#
#     # 将结果转换回字典列表
#     grouped_data = grouped.to_dict('records')
#
#     return grouped_data

# def aggregate_data(data_list, group_field, agg_fields):
#     """
#     :param data_list: 列表
#     :param group_field: 分组规则
#     :param agg_fields: 要求和的字段列表
#     """
#     # 将数据转换为 DataFrame
#     df = pd.DataFrame(data_list)
#
#     # 将累加字段转换为数值型
#     for field in agg_fields:
#         df[field] = pd.to_numeric(df[field], errors='coerce')  # 处理可能的NaN值
#
#     # 将NaN值替换为0
#     df.fillna(0, inplace=True)
#
#     # 根据 group_field 对数据进行分组，并对 agg_fields 进行求和
#     grouped = df.groupby(group_field, as_index=False)[agg_fields].sum()
#
#     return grouped.to_dict('records')

def aggregate_data(data_list, group_field, agg_fields, agg_result_field):
    """
    :param data_list: 列表
    :param group_field: 分组规则
    :param agg_fields: 要求和的字段列表
    """
    # 将数据转换为 DataFrame
    df = pd.DataFrame(data_list)

    # 将累加字段转换为数值型
    for field in agg_fields:
        df[field] = pd.to_numeric(df[field], errors='coerce')  # 处理可能的NaN值

    # 将NaN值替换为0
    df.fillna(0, inplace=True)

    # 根据 group_field 对数据进行分组，并对 agg_fields 进行求和
    df[agg_result_field] = df.groupby(group_field)[agg_fields].transform('sum')

    # 选择需要的字段
    grouped_data = df.drop(agg_fields, axis=1).drop_duplicates(subset=group_field).to_dict('records')

    return grouped_data


# json模板替换
def replace_placeholders(data, replacements):
    """
   :param data: 要替换的数据
   :param replacements: 要替换的字典
   """
    # 将 data 转换为 JSON 格式的字符串
    data_str = str(data)

    # 依次替换每一个 "{{}}"
    for replacement in replacements:
        data_str = data_str.replace("{{}}", replacement, 1)

    # 将字符串重新转换为字典
    data = eval(data_str)

    return data


# 获取程序运行时间
def testRunTime():
    start = datetime.now()
    for i in range(1000):
        for j in range(500):
            m = i + j
            print(m)
    end = datetime.now()
    print(end - start)
    return end - start


# 将dict转换为json
def convert_dict_to_json(data):
    """
     :param data: 要转换的字典
     """

    def convert_values_to_str(value):
        if isinstance(value, dict):
            return {convert_values_to_str(key): convert_values_to_str(val) for key, val in value.items()}
        elif isinstance(value, list):
            return [convert_values_to_str(val) for val in value]
        elif isinstance(value, Decimal):
            return str(value)
        elif value is None:
            return value
        else:
            return str(value)

    converted_data = convert_values_to_str(data)
    json_str = json.dumps(converted_data, ensure_ascii=False)
    return json_str


# for 列表搜索
def search_in_dict_list(dict_list, query_dict):
    """
     :param dict_list: 要过滤的列表
     :param query_dict: 要筛选的字典
     """
    return [d for d in dict_list if all(d.get(k) == v for k, v in query_dict.items())]


# Pandas库 列表搜索(支持模糊搜索)
def search_in_dict_list(dict_list, query_dict):
    """
   :param dict_list: 要过滤的列表
   :param query_dict: 要筛选的字典
   """
    df = pd.DataFrame(dict_list)
    original_length = len(df)

    for key, value in query_dict.items():
        if isinstance(value, str):
            df = df[df[key].str.contains(value)]
        else:
            df = df[df[key] == value]

    not_matching_count = original_length - len(df)
    return df.to_dict('records'), not_matching_count


# 字典过滤
def filter_dict_by_keys(dict_obj, keys):
    """
    :param dict_obj: 要过滤的字典
    :param keys: 要筛选的字段列表
    """
    keys_set = set(keys)  # Convert list to set
    return {k: v for k, v in dict_obj.items() if k in keys_set}


# 列表字段提取
def extract_values(dict_list, key):
    """
    :param dict_list: 要提取的列表
    :param key: 需要提前的key
    """
    if not dict_list:  # 如果dict_list为空，则返回空列表
        return []
    df = pd.DataFrame(dict_list)
    return df[key].tolist()


# 替换sql里面的占位符
def generate_query_string(query_string, param_list):
    """
      :param query_string: 要替换的字符串
      :param param_list: 替换的列表
      """
    # 替换问号
    for param in param_list:
        query_string = query_string.replace('?', str(param), 1)
    return query_string


# 根据支付宝微信规则生成28位不重复的交易号
def generate_trade_no():
    # 生成不重复的UUID
    trade_no = str(uuid.uuid4().int)
    # 判断交易号长度，不足补0
    if len(trade_no) < 28:
        trade_no = trade_no.zfill(28)
    # 根据支付宝和微信的规则进行格式化
    # trade_no = trade_no[:4] + '-' + trade_no[4:8] + '-' + trade_no[8:12] + '-' + trade_no[12:20] + '-' + trade_no[20:]
    trade_no = trade_no[:4] + trade_no[4:8] + trade_no[8:12] + trade_no[12:20] + trade_no[20:]

    if len(trade_no) < 28:
        trade_no = trade_no.zfill(28)
    return trade_no


# 生成合同编码
def generate_code(code_prefix):
    """
    :param code_prefix: 自定义字符串
    """
    code_date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    code_random = str(random.randint(10000, 99999))
    return f"{code_prefix}_{code_date}_{code_random}"


# 根据中文生成大写缩写
def get_chinese_initials(chinese):
    """
      :param chinese: 中文
    """
    chinese_pinyin = pinyin.get(chinese, format='strip', delimiter=' ')
    initials = [p[0].upper() for p in chinese_pinyin.split()]
    return ''.join(initials)
