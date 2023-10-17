import sys
import time
import os
import datetime

from django.forms.models import model_to_dict

from ..utils.utility_method import custom_sort
from ..models import *
from django.db.models import Q, F


class InvoiceHeaderService:

    @staticmethod
    def list(params):

        user_id = params.pop("user_id", "")
        sort = params.pop("sort", "-id")
        sort = sort if sort and sort in ["-id", "-sort", "id", "sort"] else "-id"

        currencies = InvoiceHeader.objects.filter(user_id=user_id, is_delete=0).order_by(
            sort)
        data = list(currencies.values('id', 'head_type', 'company_name', 'tax_number', 'address', 'phone_number',
                                      'account_opening_bank',
                                      'account', 'sort'))
        # 使用 custom_sort 函数进行排序，并指定需要提取排序字段的参数
        sorted_data = custom_sort(data, reverse=True, sort="sort", id="id")
        return sorted_data, None

    @staticmethod
    def edit(params):
        invoice_header_id = params.get('invoice_header_id', '')
        tax_number = params.get('tax_number', '')
        head_type = params.get('head_type', '')
        sort = params.get('sort', '')
        user_id = params.get('user_id', '')
        if not head_type:
            return None, "抬头类型不允许为空"
        if head_type == "CORPORATIONS" and not tax_number:
            return None, "税号不允许为空"
        if tax_number:
            invoice_header_set = InvoiceHeader.objects.filter(Q(tax_number=tax_number) & ~Q(id=invoice_header_id))
            if invoice_header_set.first():
                return None, "税号已存在"
        if sort:
            InvoiceHeader.objects.filter(user_id=user_id).update(**{"sort": 0})
        try:
            params.pop("invoice_header_id")
            InvoiceHeader.objects.filter(id=invoice_header_id).update(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def detail(params):
        invoice_header_id = params.get('invoice_header_id', '')
        if not invoice_header_id:
            return None, "id不能为空"
        try:
            invoice_header_set = InvoiceHeader.objects.filter(id=invoice_header_id).first()
            if invoice_header_set:
                return model_to_dict(invoice_header_set), None
            else:
                return None, "数据不存在"
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def delete(params):
        invoice_header_id = params.get('invoice_header_id', '')
        try:
            InvoiceHeader.objects.filter(id=invoice_header_id).update(**{"is_delete": 1})
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def add(params):
        tax_number = params.get('tax_number', '')
        head_type = params.get('head_type', '')
        sort = params.get('sort', '')
        user_id = params.get('user_id', '')
        if not head_type:
            return None, "抬头类型不允许为空"
        if head_type == "CORPORATIONS" and not tax_number:
            return None, "税号不允许为空"
        if sort:
            InvoiceHeader.objects.filter(user_id=user_id).update(**{"sort": 0})
        if tax_number:
            invoice_header_set = InvoiceHeader.objects.filter(tax_number=tax_number).first()
            if invoice_header_set is not None:
                return None, "税号已存在"
        try:
            InvoiceHeader.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
