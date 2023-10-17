import json
from decimal import Decimal

from django.db.models import F
from django.forms import model_to_dict

from xj_ruoyi.utils.custom_jwt_auth import CustomJWTAuthentication
from xj_ruoyi.views.dept import DeptViewSet
from ..models import *
from utils.custom_tool import filter_result_field
from ..utils.utility_method import convert_dict_to_json, parse_integers, get_current_time, replace_dict_key, \
    search_in_dict_list, extract_values, replace_key_in_dict_replacement_dicts
from ..utils.join_list import JoinList
from xj_thread.services.thread_list_service import ThreadListService
from xj_user.services.user_service import UserService
from ..services.invoice_extend_service import InvoiceExtendService
from ..utils.custom_tool import format_params_handle, force_transform_type, dynamic_load_class, \
    write_to_log


# 自定义序列化函数
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # 将 Decimal 对象转换为字符串
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


class InvoiceService:
    authentication_classes = [CustomJWTAuthentication]

    @staticmethod
    def batch_add(params):
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        invoice_list = params.get("invoice_list")
        try:
            for item in invoice_list:
                invoice, err = InvoiceService.add(item)
                if err:
                    return None, err
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(
                e.__traceback__.tb_lineno)}'''

        return None, None

    @staticmethod
    def add(params: dict = None, **kwargs):
        """
        发票添加
        :param params: 添加参数子字典
        :param kwargs:
        :return:
        """
        # 参数整合与空值验证
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        invoice_type = InvoiceType.objects.filter(invoice_type_code=params['invoice_type_code']).first()
        if not invoice_type:
            return None, "发票类型不存在"
        invoice_status_code = params.get("invoice_status_code", "APPLY")
        invoice_status = InvoiceStatus.objects.filter(invoice_status=invoice_status_code).first()
        if not invoice_status:
            return None, "发票状态不存在"

        params['invoice_type_id'] = invoice_type.id
        params['invoice_status_id'] = invoice_status.id
        # 过滤主表修改字段
        try:
            main_form_data = format_params_handle(
                param_dict=params.copy(),
                is_remove_empty=True,
                filter_filed_list=[
                    "user_id|int",
                    "salesman_id|int",
                    "dept_id|int",
                    "thread_id|int",
                    "enroll_id_list",
                    "invoice_time|date",
                    "invoice_type_id|int",
                    "invoice_price|float",
                    "invoice_number",
                    "tax_rate",
                    "invoice_tax",
                    "invoice_untaxed",
                    "tax_number",
                    "operator_user_id|int",
                    'remark',
                    "invoice_status_id",
                    "destroy_name",
                    "destroy_date",
                    "destroy_reason",
                    "destroy_operator_id",
                    "receive_email",
                    "receive_phone",
                    "invoice_snapshot|dict",
                    "invoicing_party",
                    "invoice_voucher",
                    "invoice_header_id"

                ],
                alias_dict={},
                is_validate_type=True
            )
        except ValueError as e:
            # 模型字段验证
            return None, str(e)

        # 必填参数校验
        must_keys = ["invoice_header_id", "user_id"]
        for i in must_keys:
            if not params.get(i, None):
                return None, str(i) + " 必填"
        invoice_snapshot = {}
        # 处理快照信息
        company_address = params.get("company_address", "")  # 公司地址
        company_phone = params.get("company_phone", "")  # 公司电话
        deposit_bank = params.get("deposit_bank", "")  # 开户银行
        deposit_account = params.get("deposit_account", "")  # 开户账户
        enroll_id_list = []
        invoice_snapshot['account_info'] = {
            "company_address": company_address,
            "company_phone": str(company_phone),
            "deposit_bank": deposit_bank,
            "deposit_account": str(deposit_account)
        }
        if main_form_data.get("enroll_id_list", ""):
            enroll_id_list = parse_integers(main_form_data.get("enroll_id_list", ""))
            # 载入模块
            EnrollServices, import_err = dynamic_load_class(import_path="xj_enroll.service.enroll_services",
                                                            class_name="EnrollServices")
            assert not import_err
            enroll, err = EnrollServices.enroll_list(params={"id_list": enroll_id_list})
            if enroll:
                thread_id_list = [item.get("thread_id", None) for item in enroll['list']]
                thread_list, err = ThreadListService.search(thread_id_list,
                                                            filter_fields=['title', 'classify_value', 'classify_name'])
                if thread_list:
                    enroll['list'] = JoinList(enroll['list'], thread_list, "thread_id", "id").join()
                invoice_snapshot['enroll'] = enroll['list']

        if main_form_data.get("thread_id", ""):
            thread_id_list = [main_form_data.get("thread_id", "")]
            thread_list, err = ThreadListService.search(thread_id_list)
            if thread_list:
                invoice_snapshot['thread'] = thread_list[0]
        main_form_data['invoice_snapshot'] = json.loads(convert_dict_to_json(invoice_snapshot))
        # IO操作
        try:
            # 主表插入数据
            # main_form_data['create_time'] = InvoiceService.get_current_time()
            invoice = Invoice.objects.create(**main_form_data)
            # 扩展表 插入或更新
            add_extend_res, err = InvoiceExtendService.create_or_update(params, invoice.id)
            if err:
                write_to_log(prefix="发票--扩展表 插入或更新失败", err_obj=err)

            for enroll_id in enroll_id_list:
                InvoiceToEnroll.objects.create(**{"invoice_id": invoice.id, "enroll_id": enroll_id})

            # 载入模块
            EnrollServices, import_err = dynamic_load_class(import_path="xj_enroll.service.enroll_services",
                                                            class_name="EnrollServices")
            assert not import_err
            enroll, enroll_err = EnrollServices.enroll_edit(params={"finance_invoicing_code": "INVOICING"},
                                                            search_param={"enroll_id_list": enroll_id_list
                                                                          })
            if enroll_err:
                write_to_log(
                    prefix="开票功能",
                    content="报名id:" + str(main_form_data.get("enroll_id_list", "")),
                    err_obj=enroll_err
                )
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(
                e.__traceback__.tb_lineno)}'''

        return {"id": invoice.id}, None

    @staticmethod
    def edit(params: dict = None, invoice_id=None, search_param: dict = None, **kwargs):
        """
        发票编辑
        :param params: 修改的参数
        :param invoice_id: 需要修改的发票主键
        :param search_param: 搜索参数, 服务层根据信息等其他搜索字段检索到需要修改的数据
        :return: data, err
        """
        # 空值检查
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        invoice_id, is_pass = force_transform_type(variable=invoice_id, var_type="int")
        search_param, is_pass = force_transform_type(variable=search_param, var_type="dict", default={})
        if not invoice_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"

        # 搜索字段过滤
        if search_param:
            search_param = format_params_handle(
                param_dict=search_param,
                filter_filed_list=[
                    "invoice_id|int", "invoice_id_list|list", "thread_id|int", "thread_id_list|list",
                ],
                alias_dict={"invoice_id_list": "id__in", "thread_id_list": "thread_id__in"}
            )
        # 修改内容检查处理
        try:
            main_form_data = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                is_remove_empty=True,
                filter_filed_list=[
                    "user_id|int",
                    "salesman_id|int",
                    "dept_id|int",
                    "thread_id|int",
                    "enroll_id_list",
                    "invoice_time|date",
                    "invoice_type_id|int",
                    "invoice_price|float",
                    "invoice_number",
                    "tax_rate",
                    "invoice_tax",
                    "invoice_untaxed",
                    "tax_number",
                    "operator_user_id|int",
                    'remark',
                    "invoice_status_id",
                    "destroy_name",
                    "destroy_date",
                    "destroy_reason",
                    "destroy_operator_id",
                    "receive_email",
                    "receive_phone",
                    "invoice_snapshot|dict",
                    "invoicing_party",
                    "invoice_voucher",
                    "invoice_header_id"

                ],
            )
        except ValueError as e:
            return None, str(e)
        # 构建ORM，检查是否存在可修改项目
        invoice_obj = Invoice.objects
        if invoice_id:
            invoice_obj = invoice_obj.filter(id=invoice_id)
        elif search_param:
            invoice_obj = invoice_obj.filter(**search_param)

        update_total = invoice_obj.count()
        if update_total == 0:
            return None, "没有找到可修改项目"

        # IO 操作
        try:
            main_form_data.pop("invoice_id", None)
            main_form_data['update_time'] = get_current_time()
            invoice_obj.update(**main_form_data)
            add_extend_res, err = InvoiceExtendService.create_or_update(params, invoice_id)
            if err:
                write_to_log(prefix="发票--扩展表 插入或更新失败", err_obj=err)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return invoice_obj.first().to_json(), None

    @staticmethod
    def list(params):
        not_matching_count = 0
        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10
        invoice = Invoice.objects
        # invoice = invoice.order_by('-invoice_time')
        invoice = invoice.order_by('-id')
        if params.get("is_all", 0) >= 1 or params.get("user_id_list", ""):
            # params.pop("user_id")
            params.pop("operator_user_id", None)
        if params.get("enroll_id_list", []):
            id_list_set = InvoiceToEnroll.objects.filter(enroll_id__in=params.get("enroll_id_list")).values(
                "invoice_id")
            id_list = extract_values(id_list_set, "invoice_id")
            invoice = invoice.filter(id__in=id_list)
        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "id_list|list", "thread_id|int", "user_id|int", "salesman_id|int",
                "dept_id|int", "invoice_type_code",
                "thread_id_list|list", "user_id_list|list", "head_type", "operator_user_id",
                "invoice_number", "dept_id", "dept_id_list", "company_name",
                "create_time_start", "create_time_end",
                "invoice_time_start", "invoice_time_end", "invoice_status_code"
            ],
            split_list=["thread_id_list", "id_list", "user_id_list"],
            alias_dict={
                "create_time_start": "create_time_gte", "create_time_end": "create_time__lte",
                "invoice_time_start": "invoice_time__gte", "invoice_time_end": "invoice_time__lte",
                "dept_id_list": "dept_id__in",
                "thread_id_list": "thread_id__in", "id_list": "id__in", "user_id_list": "user_id__in",
                "invoice_type_code": "invoice_type__invoice_type_code__iexact",
                "invoice_status_code": "invoice_status__invoice_status__iexact",
                "head_type": "invoice_header__head_type__iexact",
                "company_name": "invoice_header__company_name__iexact"
            },
        )
        invoice = invoice.extra(select={'invoice_time': 'DATE_FORMAT(invoice_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        invoice = invoice.extra(select={'destroy_date': 'DATE_FORMAT(destroy_date, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        invoice = invoice.annotate(invoice_type_code=F("invoice_type__invoice_type_code"),
                                   invoice_type_value=F("invoice_type__invoice_type_value"))
        invoice = invoice.annotate(invoice_status_code=F("invoice_status__invoice_status"),
                                   invoice_status_value=F("invoice_status__invoice_status_value"))
        invoice = invoice.annotate(head_type=F("invoice_header__head_type"),
                                   company_name=F("invoice_header__company_name"),
                                   head_tax_number=F("invoice_header__tax_number"),
                                   address=F("invoice_header__address"),
                                   phone_number=F("invoice_header__phone_number"),
                                   account_opening_bank=F("invoice_header__account_opening_bank"),
                                   account=F("invoice_header__account"), )
        invoice = invoice.filter(**params).values()
        total = invoice.count()
        #
        current_page_set = invoice[page * size: page * size + size] if page >= 0 and size > 0 else invoice
        res_list = []
        for i, it in enumerate(current_page_set):
            it['order'] = page * size + i + 1
            it['invoice_time'] = it['invoice_time'].strftime("%Y-%m-%d %H:%M:%S") if it['invoice_time'] else it[
                'invoice_time']
            it['create_time'] = it['create_time'].strftime("%Y-%m-%d %H:%M:%S") if it['create_time'] else it[
                'create_time']
            it['update_time'] = it['update_time'].strftime("%Y-%m-%d %H:%M:%S") if it['update_time'] else it[
                'update_time']

            res_list.append(it)

        data = res_list

        # ========== 四、相关前置业务逻辑处理 ==========

        # ========== 五、翻页 ==========

        salesman_id_list = [item.get("salesman_id", "") for item in res_list]
        salesman_id_list, err = UserService.user_list(allow_user_list=salesman_id_list)
        if salesman_id_list:
            data = JoinList(res_list, salesman_id_list['list'], "salesman_id", "user_id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "invoice_id", "invoice_status_value": "invoice_status",
                            "nickname": "salesman_nickname", "user_name": "salesman_name",
                            "full_name": "salesman_full_name"},
            ),
        )
        user_id_list = [item.get("user_id", "") for item in res_list]
        user_list, err = UserService.user_list(allow_user_list=user_id_list)
        if user_list:
            data = JoinList(data, user_list['list'], "user_id", "user_id").join()

        dept_id_list = [item.get("dept_id", "") for item in res_list]
        dept_list, err = DeptViewSet.details(dept_list=dept_id_list)
        if dept_list:
            data = JoinList(data, dept_list, "dept_id", "id").join()
        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "dept_id", "name": "dept_name"},
            ),
        )
        # ======================= 信息模块适配 start ==============================
        thread_id_list = [item.get("thread_id", None) for item in data]
        thread_list, err = ThreadListService.search(thread_id_list, filter_fields="title")
        if thread_list:
            data = JoinList(data, thread_list, "thread_id", "id").join()
        # ======================= 信息模块适配 end ==============================

        # ======================= 发票扩展字段适配 start ==============================
        extend_id_list = [item.get("invoice_id", None) for item in data]
        extend_list, err = InvoiceExtendService.get_extend_info(extend_id_list)
        if extend_list:
            data = JoinList(data, extend_list, "invoice_id", "invoice_id_id").join()
        # ======================= 发票扩展字段适配 end ==============================
        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': data, }, None

    @staticmethod
    def detail(params):
        invoice_id = params.get("invoice_id")
        invoice_number = params.get("invoice_number")
        if not invoice_id and not invoice_number:
            return None, "发票信息不能为空"
        if invoice_id:
            invoice = Invoice.objects.filter(id=invoice_id)
        else:
            invoice = Invoice.objects.filter(invoice_number=invoice_number)

        invoice = invoice.extra(select={'invoice_time': 'DATE_FORMAT(invoice_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                        'create_time': 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                        'update_time': 'DATE_FORMAT(update_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        invoice = invoice.first()
        if not invoice:
            return None, "无法找到要查询的数据，请检查参数"
        data = model_to_dict(invoice)
        data = replace_dict_key(data, 'id', 'invoice_id')
        invoice_type = InvoiceType.objects.filter(id=data['invoice_type']).first()
        if invoice_type:
            data.update(model_to_dict(invoice_type))
            data = replace_dict_key(data, 'id', 'invoice_type_id')
        invoice_status = InvoiceStatus.objects.filter(id=data['invoice_status']).first()
        if invoice_status:
            data.update(model_to_dict(invoice_status))
            data = replace_dict_key(data, 'id', 'invoice_status_id')
        invoice_header = InvoiceHeader.objects.filter(id=data['invoice_header']).values("head_type", "company_name",
                                                                                        "tax_number", "address",
                                                                                        "phone_number",
                                                                                        "account_opening_bank",
                                                                                        "account").first()
        if invoice_header:
            data.update(invoice_header)

        salesman_id_list = [data.get("salesman_id", None)]
        salesman_list, err = UserService.user_list(allow_user_list=salesman_id_list)
        if salesman_list:
            if salesman_list['list']:
                data.update(salesman_list['list'][0])
                data = replace_key_in_dict_replacement_dicts(data, {
                    "nickname": "salesman_nickname",
                    "user_name": "salesman_name",
                    "full_name": "salesman_full_name"})
        user_id_list = [data.get("user_id", None)]
        user_list, err = UserService.user_list(allow_user_list=user_id_list)
        if user_list:
            if user_list['list']:
                data.update(user_list['list'][0])
        thread_id_list = [data.get("thread_id", None)]
        thread_list, err = ThreadListService.search(thread_id_list, filter_fields="title")
        if thread_list:
            data.update(thread_list[0])
        dept_id_list = [data.get("dept_id", None)]
        dept_list, err = DeptViewSet.details(dept_list=dept_id_list)
        if dept_list:
            data.update(dept_list[0])
            data = replace_key_in_dict_replacement_dicts(data, {
                "id": "dept_id",
                "name": "dept_name"})

        extend_id_list = [data.get("invoice_id", None)]
        extend_list, err = InvoiceExtendService.get_extend_info(extend_id_list)
        if extend_list:
            data.update(extend_list[0])
        return data, None

    @staticmethod
    def examine_approve(params):
        invoice_id = params.get("invoice_id", 0)
        invoice_status = params.get("invoice_status_code", "")
        invoice_number = params.get("invoice_number", "")
        invoice_time = params.get("invoice_time", "")
        data = {}
        if not invoice_id:
            return None, "发票id不能为空"
        if invoice_status not in ["APPLY", "INVOIC", "RETURN", "CANCEL"]:
            return None, "未支持发票状态"

        invoice_status = InvoiceStatus.objects.filter(invoice_status=invoice_status).first()
        if not invoice_status:
            return None, "发票状态不存在"
        data['invoice_status_id'] = invoice_status.id
        data['invoice_number'] = invoice_number
        data['invoice_time'] = invoice_time
        invoice_set = Invoice.objects.filter(id=invoice_id)
        invoice_update = invoice_set.update(**data)
        if not invoice_update:
            return None, "审核失败"
        invoice_obj = invoice_set.first()
        invoice_obj = model_to_dict(invoice_obj)
        enroll_id_list = parse_integers(invoice_obj.get("enroll_id_list", ""))
        # 载入模块
        EnrollServices, import_err = dynamic_load_class(import_path="xj_enroll.service.enroll_services",
                                                        class_name="EnrollServices")
        assert not import_err
        enroll, err = EnrollServices.enroll_edit(params={"finance_invoicing_code": "INVOICED"},
                                                 search_param={"enroll_id_list": enroll_id_list
                                                               })
        if err:
            write_to_log(
                prefix="开票功能",
                content="报名id:" + str(invoice_obj.get("enroll_id_list", "")),
                err_obj=err
            )
        return invoice_obj, None
