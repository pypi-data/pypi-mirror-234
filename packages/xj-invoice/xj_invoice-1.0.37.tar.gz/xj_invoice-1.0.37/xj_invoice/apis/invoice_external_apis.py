# _*_coding:utf-8_*_

import os, logging, time, json, copy

from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.invoice_service import InvoiceService

logger = logging.getLogger(__name__)


class InvoiceExternalApi(APIView):  # 或继承(APIView)

    # 发票添加
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("user_id", user_id)  # 用户ID
        invoice_set, err = InvoiceService.add(params)
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
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID

        invoice_set, err = InvoiceService.list(params)

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
        invoice_set, err = InvoiceService.detail(params.get("invoice_id", 0))
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

