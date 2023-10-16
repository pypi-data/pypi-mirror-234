# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
from cmath import cos
import datetime
import difflib
import inspect
import json
from logging import getLogger
from math import sin, asin, sqrt
import random
import sys
import time
from urllib.parse import parse_qs
import uuid

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from numpy.core._multiarray_umath import radians
from rest_framework.request import Request
import xmltodict


def is_number(s):
    """识别任何语言的数字字符串"""
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# json 结果集返回
def parse_json(result):
    if not result is None:
        if type(result) is str:
            try:
                result = json.loads(result.replace("'", '"').replace('\\r', "").replace('\\n', "").replace('\\t', "").replace('\\t', ""))
            except Exception as e:
                return result
        if type(result) is list:
            for index, value in enumerate(result):
                result[index] = parse_json(value)
        if type(result) is dict:
            for k, v in result.items():
                result[k] = parse_json(v)
    return result


# 函数参数解析，返回变量字典
def service_params_adapter(func, params):
    """
    获取函数的参数值，并且逐一进行赋值
    如果有**kwarg则直接进行拆包传值如：**params
    """
    res_dict = {}

    has_var_keyword = False
    inspect_obj = inspect.signature(func)
    for k, v in inspect_obj.parameters.items():
        if v.kind == inspect.Parameter.VAR_KEYWORD:
            has_var_keyword = True
        res_dict[k] = __service_params_adapter_handle(k, v, params)
    res_dict = params if has_var_keyword else res_dict
    return res_dict


# 判断参数是否有默认值
def __service_params_adapter_handle(params_name, param_obj, params):
    """
    判断参数是否有默认值
    如果有默认值并且没有传这个参数则使用默认值，有值返回该值，没有默认值并且没有传值则返回None
    :param params_name:
    :param param_obj:
    :param params:
    :return: res
    """
    res = None
    if not param_obj.default == inspect._empty:
        res = param_obj.default
    if params.get(params_name):
        res = params.get(params_name)
    return res


# 过滤list内容，白名单、黑名单、别名
def format_list_handle(param_list, filter_filed_list=None, remove_filed_list=None, alias_dict=None, remove_repeat=True):
    """
    过滤list内容
    :param param_list: 传入 param_list
    :param filter_filed_list: 需要的字段
    :param remove_filed_list: 需要删除的列表
    :param alias_dict: 元素起别名
    :return:param_list： 处理后的 param_list
    """
    if not param_list:
        return param_list
    # 类型判断 过滤字段
    if filter_filed_list and isinstance(filter_filed_list, list):
        param_list = [i for i in param_list if i in filter_filed_list]

    # 类型判断， 剔除字段
    if remove_filed_list and isinstance(remove_filed_list, list):
        param_list = [j for j in param_list if not j in remove_filed_list]

    # 类型判断 字段转换
    if alias_dict and isinstance(alias_dict, dict):
        param_list = [alias_dict.get(k, k) for k in param_list]

    # 进行去重
    if remove_repeat:
        param_list = list(set(param_list))

    return param_list


# 强制转换类型数据
def force_transform_type(variable=None, var_type: str = "str"):
    """
    强制转换类型
    :param variable:变量
    :param var_type: 需要转换的类型
    :return: transform_variable, is_err
    """
    try:
        if var_type == "str":
            return str(variable), None
        elif var_type == "int":
            return int(variable), None
        elif var_type == "bool":
            return bool(variable), None
        elif var_type == "float":
            return float(variable), None
        elif var_type == "date":
            return datetime.datetime.strptime(variable, '%Y-%m-%d %H:%M:%S')
        else:
            return str(variable), None
    except ValueError as e:
        return None, True


# 处理字典：白名单、黑名单、别名、移除空值、筛选类型
# 创建查询条件
def format_params_handle(
        param_dict: dict,
        filter_filed_list: list = None,
        remove_filed_list: list = None,
        alias_dict: dict = None,
        split_list: list = None,
        split_char: str = ";",
        is_remove_null: bool = True,
        is_remove_empty: bool = False
) -> dict:
    """
    字段筛选并替换成别名
    :param param_dict: 参数值
    :param filter_filed_list: 字段白名单，如:["id":int]
    :param remove_filed_list: 字段黑名单,["id",....]
    :param alias_dict: 别名字典, {"id":"user_id"}
    :param split_char: 字符串拆分依据
    :param split_list: 拆分字符换,该参数为了适配使用符号分割成列表。["id_list",....]
    :param is_remove_null:  是否把带有None的值移除掉
    :param is_remove_empty: 是否移除value类型等于False的字段,移除"",0,"0",None
    :return: param_dict
    """
    # 转换的数据类型不符合，直接返回出去
    if not isinstance(param_dict, dict):
        raise Exception("param_dict 必须是字典格式")

    # 过滤字段并且得数据类型映射
    new_filter_filed_list = []  # 拆分字段类型的白名单
    must_type_map = {}  # 从白名单中拆分出字段与类型的映射
    if filter_filed_list and isinstance(filter_filed_list, list):
        for i in filter_filed_list:
            key_type_list = i.split("|", 1)
            [key, key_type] = key_type_list if len(key_type_list) == 2 else [key_type_list[0], None]  # 如果为类型None，则默认是字符串
            must_type_map[key] = key_type
            new_filter_filed_list.append(key)
        param_dict = {k: v for k, v in param_dict.copy().items() if k in new_filter_filed_list and (not is_remove_empty or v) and (not is_remove_null or not v is None)}
    # 剔除字段
    if remove_filed_list and isinstance(remove_filed_list, list):
        param_dict = {k: v for k, v in param_dict.copy().items() if not k in remove_filed_list and (not is_remove_empty or v) and (not is_remove_null or not v is None)}
    # 别名替换
    if alias_dict and isinstance(alias_dict, dict):
        param_dict = {alias_dict.get(k, k): v for k, v in param_dict.copy().items()}
    # 字段拆分
    if split_list and isinstance(split_list, list):
        param_dict = {k: (v.split(split_char) if k in split_list and isinstance(v, str) else v) for k, v in param_dict.copy().items()}
    # 类型转换
    if must_type_map and isinstance(must_type_map, dict):
        for k, v in param_dict.copy().items():
            var_type = must_type_map[k] if must_type_map.get(k, None) else v
            v, is_err = force_transform_type(v, var_type)
            if is_err:
                param_dict.pop(k)
    return param_dict


make_queries_condition = format_params_handle


# 处理字典列表，白名单、黑名单、别名
def filter_result_field(result_list, filter_filed_list=None, remove_filed_list=None, alias_dict=None):
    # 转换的数据类型不符合，直接返回出去
    if not filter_filed_list and not remove_filed_list and not alias_dict:
        return result_list
    result = []
    for item in result_list:
        # 类型判断 过滤字段
        if filter_filed_list and isinstance(filter_filed_list, list):
            item = {k: v for k, v in item.copy().items() if k in filter_filed_list}
        # 类型判断， 剔除字段
        if remove_filed_list and isinstance(remove_filed_list, list):
            item = {k: v for k, v in item.copy().items() if not k in remove_filed_list}
        # 类型判断 字段转换
        if alias_dict and isinstance(alias_dict, dict):
            item = {alias_dict.get(k, k): v for k, v in item.copy().items()}
        if item:
            result.append(item)
    return result


# 请求参数解析
def parse_data(request):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
    method = request.method
    if content_type == "text/plain" or method == "GET":
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
        except Exception:
            data = request.GET
            if not data:
                data = request.POST
            if not data:
                data = {}
    elif content_type == "application/json":
        return json.loads(request.body)
    elif content_type == "multipart/form-data":
        data = request.POST
    elif content_type == "application/xml":
        try:
            data = xmltodict.parse(request.body)
            return data.get("body") or data.get("data", {})
        except Exception as e:
            data = {}
    elif content_type == "application/x-www-form-urlencoded":
        data = parse_qs(request.body.decode())
        if data:
            data = {k: v[0] for k, v in data.items()}
        else:
            data = {}

    else:
        data = getattr(request, 'data', {})
    return {k: v for k, v in data.items()}


# 请求参数解析
def request_params_wrapper(func):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    def wrapper(instance, arg_request=None, *args, request=None, **kwargs):
        """
        解析request参数，适配多种body格式。
        PS :注意使用该装饰器之后必搭配*args，**kwargs须使用
        @param instance 实例是一个APIView的实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance, request, *args, request=request, request_params={}, **kwargs, )

        # 参数解析
        content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
        method = request.method
        if content_type == "text/plain" or method == "GET":  # 不指定则默认这种content-type
            try:
                body = request.body.decode("utf-8")
                data = json.loads(body)
            except Exception as e:
                # 允许get请求的query参数传json格式字符串，如：?group_list=["basics","bid-online"]
                data = parse_json(request.GET.dict())
                if not data:
                    data = request.POST
                if not data:
                    data = {}
        elif content_type == "application/json":
            data = json.loads(request.body)
        elif content_type == "multipart/form-data":
            data = request.POST
        elif content_type == "application/xml":
            try:
                data = xmltodict.parse(request.body)
                data = data.get("body") or data.get("data", {})
            except Exception as e:
                data = {}
        elif content_type == "application/x-www-form-urlencoded":
            data = parse_qs(request.body.decode())
            if data:
                data = {k: v[0] for k, v in data.items()}
            else:
                data = {}
        else:
            data = getattr(request, 'data', {})
        # 闭包抛出
        return func(instance, request, *args, request=request, request_params={k: v for k, v in data.items()}, **kwargs)

    return wrapper


# 随机发牌
def deal_equally(total: int, num: int):
    """
    发牌均分，发完截至, 然后打乱顺序
    如：5张牌发给三个人，则是2、2、1,然后打顺序，三个人中任何一个人可能得到一张牌。
    :param total: 总数
    :param num: 平均分配给这些人
    :return: list
    """
    every_one_jetton = int((total / num))
    overplus_jetton = total % num
    jetton_list = [every_one_jetton for i in range(num)]
    if overplus_jetton == 0:
        return jetton_list
    for index in range(overplus_jetton):
        jetton_list[index] = every_one_jetton + 1
    random.shuffle(jetton_list)
    return jetton_list


# 写入日志
def write_to_log(level="info", prefix="系统异常", content="", err_obj=None):
    """
    写入日志, 注意仅仅支持python3.0以上版本
    :param level: 写入错误日志等级
    :param prefix: 提示错误类型
    :param content: 错误内容
    :param err_obj: try except 捕捉到的错误对象
    :return: data, err_msg
    """
    logger = getLogger('log')
    try:
        if not err_obj is None:
            logger.error(
                '---' + prefix + ":" + str(err_obj) + ";" +
                (" content:" + str(content) + ";" if content else "") +
                " line:" + str(err_obj.__traceback__.tb_lineno) + ";" +
                " file:" + str(err_obj.__traceback__.tb_frame.f_globals["__file__"]) + ";" +
                " datetime:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + ";"
            )

        if level == "info":
            logger.error('---' + prefix + ":" + str(content))
        elif level == "error":
            logger.error('---' + prefix + ":" + str(content))
        return True, None
    except Exception as err:
        return False, str(err)


# 流程调用装饰器
def flow_service_wrapper(func):
    """
    API 流程中间件装饰器
    PS 该装饰器必须配套request_params_wrapper装饰一起使用
    """
    if not sys.modules.get("xj_flow.services.flow_process_service.FlowProcessService"):
        from xj_flow.services.flow_process_service import FlowProcessService

    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    def wrapper(instance, arg_request=None, *args, request=None, request_params=None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        :param request_params: 请求参数解析
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request_params is None:
            request_params = {}
        flow_node_id = request_params.pop("flow_node_id", None)
        flow_action_id = request_params.pop("flow_action_id", None)
        if not flow_node_id or not flow_action_id:
            return func(instance, *args, request=request, request_params=request_params, **kwargs, )

        service = FlowProcessService()
        data, err = service.do_once_flow_in_service(flow_node_id, flow_action_id, source_params=request_params)
        if err:
            write_to_log(prefix="流程装饰器调用异常:", content=err)
        request_params = data.get("source_params", request_params)
        return func(instance, *args, request=request, request_params=request_params, **kwargs, )

    return wrapper


# 计算经纬度距离
def geodistance(lng1, lat1, lng2, lat2):
    """
    计算经纬度距离
    :param lng1: 经度1
    :param lat1: 维度1
    :param lng2: 经度2
    :param lat2: 维度2
    :return: 计算距离
    """
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance / 1000, 3) * 1000
    return distance


# 计算文本相似度
def string_similar(s1, s2):
    """
    计算字符串s1与s2的差别
    :param s1: 字符串1
    :param s2: 字符串2
    :return: 两者差异度相同位1
    """
    return difflib.SequenceMatcher(None, s1, s2).ratio()


# 生成随机字符串，2千万次重复两次。
def get_short_id(length=8):
    """
    生成随机字符串，2千万次重复两次。
    :param length:
    :return: 随机字符串
    """
    length = 8 if length > 8 else length
    dictionary = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    ]
    random_id = str(uuid.uuid4()).replace("-", '')  # 注意这里需要用uuid4
    buffer = []
    for i in range(0, length):
        start = i * 4
        end = i * 4 + 4
        val = int(random_id[start:end], 16)
        buffer.append(dictionary[val % 62])
    return "".join(buffer)
