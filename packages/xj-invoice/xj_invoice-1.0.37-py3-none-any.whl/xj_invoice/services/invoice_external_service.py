from decimal import Decimal

from django.db.models import F
from django.forms import model_to_dict
from xj_thread.services.thread_list_service import ThreadListService
from ..utils.custom_tool import format_params_handle, force_transform_type

from ..models import *
from ..utils.join_list import JoinList
from xj_migrate.utils.utility_method import replace_dict_key


# 自定义序列化函数
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # 将 Decimal 对象转换为字符串
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


class InvoiceExternalService:

    @staticmethod
    def add(params: dict = None, **kwargs):
        """
        发票-外经证添加
        :param params: 添加参数子字典
        :param kwargs:
        :return:
        """
        # 参数整合与空值验证
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        # 过滤主表修改字段
        try:
            main_form_data = format_params_handle(
                param_dict=params.copy(),
                is_remove_empty=True,
                filter_filed_list=[
                    "thread_id|int",
                    "external_number",
                    "create_date|date",
                    "external_status_id|int",
                    "invoice_price|float",
                    "external_price",
                    "tax_date|date",
                    "end_date|date",
                    "external_address",
                    "remark",
                    "return_date|date",
                    'destroy_name',
                    "destroy_date"
                ],
                alias_dict={},
                is_validate_type=True
            )
        except ValueError as e:
            # 模型字段验证
            return None, str(e)

        # 必填参数校验
        must_keys = ["thread_id"]
        for i in must_keys:
            if not params.get(i, None):
                return None, str(i) + " 必填"

        # IO操作
        try:
            invoice_external = InvoiceExternal.objects.create(**main_form_data)
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(
                e.__traceback__.tb_lineno)}'''

        return {"id": invoice_external.id}, None

    @staticmethod
    def edit(params: dict = None, external_id=None, search_param: dict = None, **kwargs):
        """
        发票-外经证编辑
        :param params: 修改的参数
        :param external_id: 需要修改的外经证主键
        :param search_param: 搜索参数, 服务层根据信息等其他搜索字段检索到需要修改的数据
        :return: data, err
        """
        # 空值检查
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        external_id, is_pass = force_transform_type(variable=external_id, var_type="int")
        search_param, is_pass = force_transform_type(variable=search_param, var_type="dict", default={})
        if not external_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"

        # 搜索字段过滤
        if search_param:
            search_param = format_params_handle(
                param_dict=search_param,
                filter_filed_list=[
                    "external_id|int", "external_id_list|list", "thread_id|int", "thread_id_list|list",
                ],
                alias_dict={"external_id_list": "id__in", "thread_id_list": "thread_id__in"}
            )
        # 修改内容检查处理
        try:
            main_form_data = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                is_remove_empty=True,
                filter_filed_list=[
                    "thread_id|int",
                    "external_number",
                    "create_date|date",
                    "external_status_id|int",
                    "invoice_price|float",
                    "external_price",
                    "tax_date|date",
                    "end_date|date",
                    "external_address",
                    "remark",
                    "return_date|date",
                    'destroy_name',
                    "destroy_date"

                ],
            )
        except ValueError as e:
            return None, str(e)
        # 构建ORM，检查是否存在可修改项目
        external_obj = InvoiceExternal.objects
        if external_id:
            external_obj = external_obj.filter(id=external_id)
        elif search_param:
            external_obj = external_obj.filter(**search_param)

        update_total = external_obj.count()
        if update_total == 0:
            return None, "没有找到可修改项目"

        # IO 操作
        try:
            main_form_data.pop("external_id", None)
            external_obj.update(**main_form_data)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return external_obj.first().to_json(), None

    @staticmethod
    def list(params):

        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10
        external = InvoiceExternal.objects
        # invoice = invoice.order_by('-invoice_time')
        external = external.order_by('-id')
        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "id_list|list", "thread_id|int", "user_id|int", "invoice_type_code",
                "thread_id_list|list",
                "invoice_number|int",
                "invoice_time_start|date", "invoice_time_end|date", "invoice_status"
            ],
            split_list=["thread_id_list", "id_list"],
            alias_dict={
                "create_date_start": "create_date__gte", "create_date_end": "create_date__lte",
                "thread_id_list": "thread_id__in", "id_list": "id__in",
                "external_status_code": "external_status__external_status_code__iexact"
            },
        )
        external = external.annotate(external_status_code=F("external_status__external_status_code"),
                                     external_status_value=F("external_status__external_status_value"))
        external = external.filter(**params).values()
        total = external.count()
        #
        current_page_set = external[page * size: page * size + size] if page >= 0 and size > 0 else external
        res_list = []
        for i, it in enumerate(current_page_set):
            it['order'] = page * size + i + 1
            it['create_date'] = it['create_date'].strftime("%Y-%m-%d %H:%M:%S") if it['create_date'] else it[
                'create_date']
            it['tax_date'] = it['tax_date'].strftime("%Y-%m-%d %H:%M:%S") if it['tax_date'] else it[
                'tax_date']
            it['end_date'] = it['update_time'].strftime("%Y-%m-%d %H:%M:%S") if it['end_date'] else it[
                'end_date']
            it['return_date'] = it['return_date'].strftime("%Y-%m-%d %H:%M:%S") if it['return_date'] else it[
                'return_date']
            it['destroy_date'] = it['destroy_date'].strftime("%Y-%m-%d %H:%M:%S") if it['destroy_date'] else it[
                'destroy_date']
            res_list.append(it)

        data = res_list

        thread_id_list = [item.get("thread_id", None) for item in data]
        thread_list, err = ThreadListService.search(thread_id_list, filter_fields="title")
        if thread_list:
            data = JoinList(data, thread_list, "thread_id", "id").join()

        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': data, }, None

    @staticmethod
    def detail(external_id):
        if not external_id:
            return None, "外经证id不能为空"
        external = InvoiceExternal.objects.filter(id=external_id)
        external = external.extra(select={'create_date': 'DATE_FORMAT(create_date, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                          'tax_date': 'DATE_FORMAT(tax_date, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                          'end_date': 'DATE_FORMAT(end_date, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                          'return_date': 'DATE_FORMAT(return_date, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                          'destroy_date': 'DATE_FORMAT(destroy_date, "%%Y-%%m-%%d %%H:%%i:%%s")'})

        external = external.first()
        if not external:
            return None, "无法找到要查询的数据，请检查参数"
        data = model_to_dict(external)
        data = replace_dict_key(data, 'id', 'invoice_id')
        external_status = InvoiceStatus.objects.filter(id=data['external_status_id']).first()
        if external_status:
            data.update(model_to_dict(external_status))
            data = replace_dict_key(data, 'id', 'external_status_id')
        thread_id_list = [data.get("thread_id", None)]
        thread_list, err = ThreadListService.search(thread_id_list, filter_fields="title")
        if thread_list:
            data.update(thread_list[0])
        return data, None





