# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""
from cmath import cos
import copy
import datetime
import difflib
import importlib
import inspect
import json
from logging import getLogger
from math import sin, asin, sqrt
import random
import re
import sys
import time
from urllib.parse import parse_qs
import uuid

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from numpy.core._multiarray_umath import radians
from rest_framework.request import Request
import xmltodict

# =========== section 单例装饰器 start ==================
_instance = {}


# 单例装饰器
def singleton_decorator(cls, *args, **kwargs):
    def inner(*args, **kwargs):
        cls_name = cls.__name__
        if cls_name not in _instance:
            _instance[cls_name] = cls(*args, **kwargs)
        return _instance[cls_name]

    return inner


# 获取单例
def get_singleton(key):
    return _instance.get(key, {})


# =========== section 单例装饰器 end    ==================


def dynamic_load_class(import_path: str = None, class_name: str = None, find_services=False):
    """
    动态加载模块中的类,返回类的指针
    可从通过RPC协议从consul服务获取其他服务器的服务类。
    :param find_services: 是否使用RPC，发现服务
    :param import_path: 导入类的文件路径
    :param class_name: 导入文件中的哪一个类
    :return: class_instance,err_msg
    """
    try:
        class_instance = getattr(sys.modules.get(import_path), class_name, None)
        if class_instance is None:
            import_module = importlib.import_module(import_path)
            class_instance = getattr(import_module, class_name)
        copy_class_instance = copy.deepcopy(class_instance)
        return copy_class_instance, None
    except AttributeError:
        return None, "系统中不存在定位模块"
    except Exception as e:
        return None, str(e)


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
def force_transform_type(variable=None, var_type: str = None, default=None, **kwargs):
    """
    强制转换类型，转换规则如下：
    1.变量为空使用默认值返回。认为是空值判断。
    2.转换类型为空则，返回输入变量。认为不需要进行类型转换。
    3.无法转换则返回默认值，转换失败，数据存在问题则饭hi默认值。
    :param default: 数据为空或无法转换的时候返回默认值
    :param variable: 变量
    :param var_type: 转换类型 str|int|bool|float|dict|list|date
    :return: transform_variable, is_err
    """
    if variable is None:  # 为空时候，则返回默认值
        return default, None
    if not var_type:  # 转换类型为空，则不进行转换
        return variable, None
    # 强制类型转换
    try:
        if var_type == "str":
            return variable if isinstance(variable, str) else str(variable), None
        elif var_type == "int":
            return variable if isinstance(variable, int) else int(variable), None
        elif var_type == "bool":
            if variable in (None, '', [], (), {}):
                return None, None
            if variable in (True, False):
                return bool(variable), None
            if variable in ('t', 'True', '1'):
                return True, None
            if variable in ('f', 'False', '0'):
                return False, None
            return None, "'" + str(variable) + "'" + "不是一个有效的布尔类型数据"
        elif var_type == "float":
            return variable if isinstance(variable, float) else float(variable), None
        elif var_type == "only_dict":
            # 不包括列表
            variable = parse_json(variable)
            if isinstance(variable, dict):
                return variable, None
            return default, str(variable) + "无法转换为json格式"
        elif var_type == "dict":
            # 字典包括列表字典
            variable = parse_json(variable)
            if isinstance(variable, dict) or isinstance(variable, list):
                return variable, None
            return default, str(variable) + "无法转换为json格式"
        elif var_type == "list":
            variable = parse_json(variable)
            if isinstance(variable, list):
                return variable, None
            return default, str(variable) + "无法转换为list格式"
        elif var_type == "list_int":
            variable = parse_json(variable)
            result = []
            if isinstance(variable, list):
                for i in variable:
                    # 过滤掉非int类型
                    i, is_pass = force_transform_type(variable=i, var_type="int")
                    if is_pass:
                        continue
                    result.append(i)
                return result, None
            return default, str(variable) + "无法转换为list格式"
        elif var_type == "date":
            format_map = {
                '%Y-%m-%d': "%Y-%m-%d 00:00:00",
                '%Y-%m-%d %H': '%Y-%m-%d %H:00:00',
                '%Y-%m-%d %H:%M': '%Y-%m-%d %H:%M:00',
                '%Y-%m-%d %H:%M:%S': '%Y-%m-%d %H:%M:%S'
            }
            for format_input, format_output in format_map.items():
                try:
                    return datetime.datetime.strptime(variable, format_input).strftime(format_output), None
                except ValueError:
                    pass
            raise ValueError
        else:  # 如果指派的类型不存在，默认值非空则返回默认值，否则原样返回
            return variable if default is None else default, str(var_type) + "不是一个有效的转换类型"
    except TypeError:
        return default, "'" + str(variable) + "'" + "不是一个有效的" + str(var_type) + "类型数据"
    except ValueError:
        return default, "'" + str(variable) + "'" + "不是一个有效的" + str(var_type) + "类型数据"


# 处理字典：白名单、黑名单、别名、移除空值、筛选类型
def format_params_handle(
        param_dict: dict,
        filter_filed_list: list = None,
        remove_filed_list: list = None,
        alias_dict: dict = None,
        split_list: list = None,
        split_char: str = ";",
        is_remove_null: bool = True,
        is_remove_empty: bool = False,
        date_format_dict: dict = None,
        is_validate_type: bool = False,
) -> dict:
    """
    字段筛选并替换成别名
    :param is_validate_type: 是否验证数据合法性
    :param param_dict: 参数值
    :param filter_filed_list: 字段白名单，如:["id":int]
    :param remove_filed_list: 字段黑名单,["id",....]
    :param alias_dict: 别名字典, {"id":"user_id"}
    :param split_char: 字符串拆分依据
    :param split_list: 拆分字符换,该参数为了适配使用符号分割成列表。["id_list",....]
    :param is_remove_null:  是否把带有None的值移除掉
    :param is_remove_empty: 是否移除value类型等于False的字段,移除"",0,"0",None
    :param date_format_dict: 日期格式化 日期列表，{field：(from_format,to_format),}如：{"field":("%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M:%S")}
    :return: param_dict
    """
    # 转换的数据类型不符合，直接返回出去
    if not isinstance(param_dict, dict):
        raise ValueError("param_dict 必须是字典格式")
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
    # 字段拆分
    if split_list and isinstance(split_list, list):
        param_dict = {k: (str(v).split(split_char) if k in split_list and not isinstance(v, list) else v) for k, v in param_dict.copy().items()}
    # 类型转换
    if must_type_map and isinstance(must_type_map, dict):
        for k, v in param_dict.copy().items():
            v, is_err = force_transform_type(v, must_type_map.get(k, None))
            if is_err and not is_validate_type:
                param_dict.pop(k)
            elif is_err and is_validate_type:
                raise ValueError(k + ":" + is_err)
            else:
                # 覆盖掉转换的值
                param_dict[k] = v

    # 日期字段格式转换
    if date_format_dict and isinstance(date_format_dict, dict):
        for k, v in param_dict.copy().items():
            if not date_format_dict.get(k):
                continue
            try:
                from_format, to_format = date_format_dict[k]
                if not isinstance(v, datetime.datetime) and isinstance(v, str):
                    parse_date_obj = datetime.datetime.strptime(v, from_format)
                else:
                    parse_date_obj = v
                param_dict[k] = parse_date_obj.strftime(to_format)
            except Exception as e:
                pass

    # 别名替换
    if alias_dict and isinstance(alias_dict, dict):
        param_dict = {alias_dict.get(k, k): v for k, v in param_dict.copy().items()}

    return param_dict


def filter_fields_handler(
        default_field_list: list = None,
        input_field_expression: 'str|list' = None,
        split_char: str = ";",
        all_field_list: list = None
) -> list:
    """
    过滤字段处理器
    使用：服务提供者只需要提供一个默认字段的列表或者符号分割的字符串，然后再把前端传进来的字段表达式传进来即可
    :param all_field_list: 全部合法性字段
    :param default_field_list: 默认字段列表,或者是符号分割的字符串
    :param input_field_expression: 字段处理表达式。"***filed_1;filed_2;;filed_2;!!!filed_1;filed_2;" 或者"filed_1;filed_2"或者 [filed_1,filed_2;]
    :param split_char: 拆分字符串,默认使用分号。
    :return: ["field_1",.....]
    """
    # all_field_list 与 default_field_list 因为是在服务层调用，所以强制列表类型
    if all_field_list is None or not isinstance(all_field_list, list):
        all_field_list = []
    if default_field_list is None or not isinstance(default_field_list, list):
        default_field_list = []
    # 处理默认字段
    default_field_list = default_field_list.split(split_char) if isinstance(default_field_list, str) else default_field_list or all_field_list

    # ========== 处理字段处理表达式 ==========
    # 如果没有传递字段表达式，默认字段不为空。则返回默认字段
    if input_field_expression is None:
        return default_field_list

    # 字段表达式字符串的情况
    elif isinstance(input_field_expression, str):
        if not re.search("[***|!!!]", input_field_expression):
            return format_list_handle(param_list=input_field_expression.split(split_char), filter_filed_list=all_field_list)
        # 加法或者减法原则
        default_field_hash = {i: "" for i in default_field_list}
        add_filed_expression = re.search("[***][^(!!!)]*", input_field_expression)
        sub_filed_expression = re.search("[!!!][^(***)]*", input_field_expression)
        if add_filed_expression:
            add_filed_list = add_filed_expression.group().replace("***", "").split(split_char)
            for i in add_filed_list:
                default_field_hash.update({i: ""})
        if sub_filed_expression:
            sub_filed_list = sub_filed_expression.group().replace("!!!", "").split(split_char)
            for i in sub_filed_list:
                default_field_hash.pop(i, None)
        return format_list_handle(param_list=[i for i in list(default_field_hash.keys()) if i], filter_filed_list=all_field_list)

    # 如果是列表则代表用户使用自定义的字段列表，不使用默认的字段列表
    elif isinstance(input_field_expression, list):
        return format_list_handle(param_list=input_field_expression, filter_filed_list=all_field_list)

    # input_field_expression的类型都不符合，则返回default_field_list
    else:
        return default_field_list
    # ========== 处理字段处理表达式 ==========


# 处理字典列表，白名单、黑名单、别名
def filter_result_field(
        result_list: list,
        filter_filed_list: list = None,
        remove_filed_list: list = None,
        alias_dict: dict = None,
        date_format_dict: dict = None
):
    """
    处理列表字典：白名单、黑名单、别名、移除空值、筛选类型等操作，把处理后的结果集返回出去。
    :param result_list: 结果集列表
    :param filter_filed_list: 白名单列表
    :param remove_filed_list: 黑名单列表
    :param alias_dict: 别名列表
    :param date_format_dict: 日期列表，{field：(from_format,to_format),}如：{"field":("%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M:%S")}
    :return: result_list
    """
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
        # 日期字段格式转换
        if date_format_dict and isinstance(date_format_dict, dict):
            for k, v in item.copy().items():
                if not date_format_dict.get(k):
                    continue
                try:
                    from_format, to_format = date_format_dict[k]
                    if not isinstance(v, datetime.datetime) and isinstance(v, str):
                        parse_date_obj = datetime.datetime.strptime(v, from_format)
                    else:
                        parse_date_obj = v
                    item[k] = parse_date_obj.strftime(to_format)
                except Exception as e:
                    pass
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


# 请求参数析解
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
        elif level == "info":
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
    PS 该装饰器必须配套request_params_wrapper 和 user_wrapper 一起使用
    PS 开放的服务必须使用key_value类型接收参数，如：params: dict = None, **kwargs
    """

    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    def wrapper(instance, arg_request=None, *args, request=None, request_params=None, user_info: dict = None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        :param user_info: 用户信息，使用用户登录验证装饰器才会生效。
        :param request_params: 请求参数解析
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request

        # ----------------- section 得到请求参数以及用户信息 start --------------------------
        user_info, is_pass = force_transform_type(variable=user_info, var_type="dict", default={})
        request_params, is_pass = force_transform_type(variable=request_params, var_type="dict", default={})
        # 自动补全，用户信息字段
        for k, v in user_info.items():
            request_params.setdefault(k, v)
        # ----------------- section 得到请求参数以及用户信息 end   --------------------------

        # ----------------- section 加载流程类,并判断是否要执行流程 start --------------------------
        CopyFlowProcessService, is_import = dynamic_load_class(import_path="xj_flow.services.flow_process_service", class_name="FlowProcessService")
        # 检查请求参数中是否由流程相关信息,判断是触发流程
        flow_node_id = request_params.pop("flow_node_id", None)
        flow_action_id = request_params.pop("flow_action_id", None)
        flow_node_value = request_params.pop("flow_node_value", None)
        flow_action_value = request_params.pop("flow_action_value", None)
        if is_import or (not flow_node_id and not flow_node_value) or (not flow_action_id and not flow_action_value):
            return func(instance, *args, request=request, request_params=request_params, user_info=user_info.copy(), **kwargs)
        # ----------------- section 加载流程类,并判断是否要执行流程 end   --------------------------

        # ----------------- section 执行前置流程方法 start --------------------------
        service = CopyFlowProcessService()
        data, err = service.do_once_flow_in_service(
            flow_node_id=flow_node_id,
            flow_node_value=flow_node_value,
            flow_action_id=flow_action_id,
            flow_action_value=flow_action_value,
            source_params=request_params.copy(),
            run_mode="BEFORE"
        )
        # 如果有错误则计入执行错误日志
        if err:
            write_to_log(prefix="流程装饰器调用异常:", content=err)
        # 处理后的参数默认值补全
        data = data or {}
        request_params = data.get("source_params", request_params)
        # ----------------- section 执行前置流程方法 end   --------------------------

        # ----------------- section 执行接口方法 start --------------------------
        response = func(instance, *args, request=request, request_params=request_params.copy(), user_info=user_info.copy(), **kwargs)
        # 获取http响应的内容
        response_json = parse_json(response.content.decode(encoding="utf-8"))
        response_json, is_pass = force_transform_type(variable=response_json, var_type="dict", default={})
        response_err = response_json.get("err", None)
        # ----------------- section 执行接口方法 end   --------------------------

        # ----------------- section 执行后置流程方法 start --------------------------
        if not response_err:
            # 如果请求接口没有报错则不可以执行
            data, err = service.do_once_flow_in_service(
                flow_node_id=flow_node_id,
                flow_node_value=flow_node_value,
                flow_action_id=flow_action_id,
                flow_action_value=flow_action_value,
                source_params=request_params.copy(),
                run_mode="AFTER"
            )
            if err:
                write_to_log(prefix="流程装饰器调用异常:", content=err)
        # ----------------- section 执行后置流程方法 end   --------------------------
        # 记录流程记录
        record, record_err = service.save_record(result_dict=response_json.get("data", {}), user_info=user_info.copy())
        if record_err:
            write_to_log(prefix="流程装饰器保存流程记录失败", content=record_err)
        return response

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


# 字典合并字段冲突，自动加前缀
def conflict_fields(source_data: "list|dict" = None, foreign_data: "list|dict" = None, prefix=""):
    """
    字典合并字段冲突，自动加前缀
    @note 注意仅仅支持{}或者[{}]格式
    :param prefix: 字段冲突添加前缀
    :param source_data: 源数据集合
    :param foreign_data: 外来数据集合
    :return: foreign_data
    """
    if (not isinstance(foreign_data, list) and not isinstance(foreign_data, dict)) or (not isinstance(source_data, list) and not isinstance(source_data, dict)):
        return foreign_data

    # 获取源数据字段名称
    source_keys = []
    if isinstance(source_data, list):
        for item in source_data:
            if isinstance(item, dict):
                source_keys += list(item.keys())
        source_keys = list(set(source_keys))
    else:
        source_keys = list(source_data.keys())

    # 获取外来数据字段key
    foreign_keys = []
    if isinstance(foreign_data, list):
        for item in foreign_data:
            if isinstance(item, dict):
                foreign_keys += list(item.keys())
        foreign_keys = list(set(foreign_keys))
    else:
        foreign_keys = list(foreign_data.keys())

    # 建立外键的映射
    conflict_fields_map = {i: str(prefix) + i for i in foreign_keys if i in source_keys}

    # 冲突字段添加前缀替换
    if isinstance(foreign_data, list):
        foreign_data = filter_result_field(
            result_list=foreign_data,
            alias_dict=conflict_fields_map
        )
    else:
        foreign_data = format_params_handle(
            param_dict=foreign_data,
            alias_dict=conflict_fields_map
        )
    return foreign_data
