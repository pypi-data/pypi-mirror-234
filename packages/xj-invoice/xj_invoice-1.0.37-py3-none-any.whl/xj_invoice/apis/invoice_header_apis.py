# _*_coding:utf-8_*_

import os, logging, time, json, copy

from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.invoice_header_service import InvoiceHeaderService
from ..services.invoice_type_service import InvoiceTypeService
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.invoice_service import InvoiceService

logger = logging.getLogger(__name__)


class InvoiceHeaderApi(APIView):  # 或继承(APIView)

    # 发票抬头添加
    @require_http_methods(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        pay_mode_set, err = InvoiceHeaderService.add(params)
        if err is None:
            return util_response(data=pay_mode_set)
        return util_response(err=47767, msg=err)

    #  发票抬头修改
    @require_http_methods(['PUT'])
    @user_authentication_wrapper
    @request_params_wrapper
    def edit(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        pay_mode_set, err = InvoiceHeaderService.edit(params)
        if err is None:
            return util_response(data=pay_mode_set)
        return util_response(err=47767, msg=err)

    #  发票抬头列表
    @require_http_methods(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        pay_mode_set, err = InvoiceHeaderService.list(params)
        if err is None:
            return util_response(data=pay_mode_set)
        return util_response(err=47767, msg=err)

    #  发票抬头列表
    @require_http_methods(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def detail(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        pay_mode_set, err = InvoiceHeaderService.detail(params)
        if err is None:
            return util_response(data=pay_mode_set)
        return util_response(err=47767, msg=err)

    # 发票抬头删除
    @require_http_methods(['DELETE'])
    @user_authentication_wrapper
    @request_params_wrapper
    def delete(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        pay_mode_set, err = InvoiceHeaderService.delete(params)
        if err is None:
            return util_response(data=pay_mode_set)
        return util_response(err=47767, msg=err)
