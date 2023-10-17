# _*_coding:utf-8_*_

import os, logging, time, json, copy

from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from xj_user.services.user_service import UserService
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper, format_params_handle, dynamic_load_class
from ..utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.invoice_service import InvoiceService
from ..utils.utility_method import extract_values

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
        if request_params is None:
            request_params = {}
        if user_info:
            request_params.setdefault("user_id", user_info.get("user_id"))
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

        # ================== 分组id列表反查询发票 start ===============================

        UserGroupService, err = dynamic_load_class(
            import_path="xj_role.services.user_group_service",
            class_name="UserGroupService"
        )
        group_id = request_params.get("group_id", "")
        if not err and group_id:
            group, err = UserGroupService.get_user_ids_by_group(group_id)
            if not err:
                request_params["user_id_list"] = group
        # ================== 分组id列表反查询发票 end ===============================

        # ================== 用户id列表反查询发票 start===============================
        DetailInfoService,  detail_info_err = dynamic_load_class(
            import_path="xj_user.services.user_detail_info_service",
            class_name="DetailInfoService"
        )
        if not detail_info_err:
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
