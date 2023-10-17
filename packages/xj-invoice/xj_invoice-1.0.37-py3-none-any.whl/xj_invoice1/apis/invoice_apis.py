# _*_coding:utf-8_*_

import logging

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper, format_params_handle, dynamic_load_class
from ..utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.invoice_service import InvoiceService
from ..utils.utility_method import extract_values, parse_integers

logger = logging.getLogger(__name__)


class InvoiceApi(APIView):  # 或继承(APIView)
    # 发票添加
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID
        invoice_set, err = InvoiceService.add(params)
        if err is None:
            return util_response(data=invoice_set)
        return util_response(err=47767, msg=err)

    # 发票批量添加
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def batch_add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        invoice_set, err = InvoiceService.batch_add(params)
        if err is None:
            return util_response(data=invoice_set)
        return util_response(err=47767, msg=err)

    # 发票修改
    @api_view(['PUT'])
    @user_authentication_wrapper
    @request_params_wrapper
    def edit(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        invoice_id = params.get("invoice_id", 0)
        invoice_set, err = InvoiceService.edit(params, invoice_id)
        if err is None:
            return util_response(data=invoice_set)
        return util_response(err=47767, msg=err)

    # 发票列表
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        data_permission = {}
        if request_params is None:
            request_params = {}
        if user_info:
            # request_params.setdefault("user_id", user_info.get("user_id"))
            user_id = user_info.get("user_id")
        else:
            return util_response(err=6001, msg="非法请求，请您登录")

        # ================== 信息id列表反查询发票 start===============================
        ThreadListService, err = dynamic_load_class(
            import_path="xj_thread.services.thread_list_service",
            class_name="ThreadListService"
        )
        thread_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["title", "subtitle", "access_level", "author", "customer_code"],
            is_remove_empty=True
        )
        if not err and thread_params:
            thread_ids, err = ThreadListService.list(params=thread_params)
            if not err:
                request_params["thread_id_list"] = extract_values(thread_ids['list'], "id")

            if isinstance(request_params.get("thread_id_list"), list) and len(request_params["thread_id_list"]) == 0:
                request_params["thread_id_list"] = [0]
        # ================== 信息id列表反查询发票 end ===============================

        # ================== 开票公司查询 start ===============================

        invoicing_company = request_params.get("invoicing_company", "")
        if invoicing_company:
            request_params["user_id_list"] = parse_integers(invoicing_company)
        print(invoicing_company)
        # ================== 开票公司查询发票 end ===============================

        # ================== 用户id列表反查询发票 start===============================
        DetailInfoService, err = dynamic_load_class(
            import_path="xj_user.services.user_detail_info_service",
            class_name="DetailInfoService"
        )
        if not err:
            user_params = format_params_handle(
                param_dict=request_params,
                filter_filed_list=["user_name"],
                is_remove_empty=True
            )
            if user_params:
                user_ids, err = DetailInfoService.get_list_detail(params=user_params)
                if not err:
                    request_params["user_id_list"] = extract_values(user_ids['list'], 'user_id')

                if isinstance(request_params.get("user_id_list"), list) and len(
                        request_params["user_id_list"]) == 0:
                    request_params["user_id_list"] = [0]
        # ================== 用户id列表反查询发票 end ===============================

        # ================== 新权限数据处理 start ===============================
        DataPermissionFilter, err = dynamic_load_class(
            import_path="xj_ruoyi.utils.data_permission",
            class_name="DataPermissionFilter"
        )
        if not err:
            data_permission = DataPermissionFilter.data_permission(user_id)
            if data_permission:
                if data_permission.get("user_id", None):
                    request_params["operator_user_id"] = data_permission.get("user_id", None)
                elif data_permission.get("user_dept_id", None):
                    request_params["dept_id"] = data_permission.get("user_dept_id", None)
                elif data_permission.get("dept_list", None):
                    request_params["dept_id_list"] = data_permission.get("dept_list", None)
                else:
                    return util_response(data=data_permission)
        # ================== 新权限数据处理 end ===============================

        invoice_set, err = InvoiceService.list(request_params)

        if err is None:
            return util_response(data=invoice_set)

        return util_response(err=47767, msg=err)

    # 发票详细
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def detail(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID
        invoice_set, err = InvoiceService.detail(params)
        if err is None:
            return util_response(data=invoice_set)
        return util_response(err=47767, msg=err)

    # 发票审批
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def examine_approve(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID
        invoice_set, err = InvoiceService.examine_approve(params)
        if err is None:
            return util_response(data=invoice_set)
        return util_response(err=47767, msg=err)
