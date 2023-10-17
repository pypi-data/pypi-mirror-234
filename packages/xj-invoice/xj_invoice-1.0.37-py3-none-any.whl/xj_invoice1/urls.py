# _*_coding:utf-8_*_
from django.urls import re_path

from .apis.invoice_apis import InvoiceApi
from .apis.invoice_header_apis import InvoiceHeaderApi
from .apis.invoice_type_apis import InvoiceTypeApi
from .service_register import register

register()

urlpatterns = [
    re_path(r'^add/?$', InvoiceApi.add, name="发票添加"),  # 发票添加
    re_path(r'^batch_add/?$', InvoiceApi.batch_add, name="发票批量添加"),  # 发票批量添加
    re_path(r'^edit/?$', InvoiceApi.edit, name="发票编辑"),  # 编辑
    re_path(r'^list/?$', InvoiceApi.list, name="发票列表"),  # 列表
    re_path(r'^detail/?$', InvoiceApi.detail, name="发票详情"),  # 详情
    re_path(r'^examine_approve/?$', InvoiceApi.examine_approve, name="发票审批"),  # 发票审批

    re_path(r'^type_list/?$', InvoiceTypeApi.list, name="发票状态列表"),  # 列表

    re_path(r'^header_add/?$', InvoiceHeaderApi.add, name="发票抬头添加"),  # 发票抬头添加
    re_path(r'^header_detail/?$', InvoiceHeaderApi.detail, name="发票抬头详情"),  # 详情
    re_path(r'^header_edit/?$', InvoiceHeaderApi.edit, name="发票抬头编辑"),  # 编辑
    re_path(r'^header_list/?$', InvoiceHeaderApi.list, name="发票抬头列表"),  # 列表
    re_path(r'^header_delete/?$', InvoiceHeaderApi.delete, name="发票抬头删除"),  # 删除
]
