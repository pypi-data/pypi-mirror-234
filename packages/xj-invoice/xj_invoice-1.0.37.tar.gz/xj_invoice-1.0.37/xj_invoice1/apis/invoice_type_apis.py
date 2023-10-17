# _*_coding:utf-8_*_

import os, logging, time, json, copy
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.invoice_type_service import InvoiceTypeService
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.invoice_service import InvoiceService

logger = logging.getLogger(__name__)


class InvoiceTypeApi(APIView):  # 或继承(APIView)

    # 发票状态列表
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID

        invoice_set, err = InvoiceTypeService.list()

        if err is None:
            return util_response(data=invoice_set)

        return util_response(err=47767, msg=err)
