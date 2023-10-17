from django.contrib import admin
# 引入用户平台
from .models import *


# #
#
class InvoiceAdmin(admin.ModelAdmin):
    fields = (
        'id', 'user_id', 'thread_id', 'invoice_time', 'invoice_type', 'invoice_number', 'invoice_price', 'tax_rate',
        'invoice_tax',
        'invoice_untaxed', 'tax_number', 'operator_user_id', 'remark', 'invoice_status', 'destroy_name', 'destroy_date',
        'destroy_reason', 'destroy_operator_id', 'receive_email', 'receive_phone', 'invoice_snapshot')
    list_display = (
        'id', 'user_id', 'thread_id', 'invoice_time', 'invoice_type', 'invoice_number', 'invoice_price', 'tax_rate',
        'invoice_tax',
        'invoice_untaxed', 'tax_number', 'operator_user_id', 'remark', 'invoice_status', 'destroy_name', 'destroy_date',
        'destroy_reason', 'destroy_operator_id', 'receive_email', 'receive_phone', 'invoice_snapshot')
    search_fields = (
        'user_id', 'invoice_number', 'invoice_type', 'receive_email')
    readonly_fields = ['id']


# #
#
class EextendFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'field_index', 'field', 'value', 'type', 'unit', 'config', 'description', 'default')
    list_display = (
        'id', 'field_index', 'field', 'value', 'type', 'unit', 'config', 'description', 'default')
    search_fields = (
        'id', 'field_index', 'field', 'value', 'type', 'unit', 'config', 'description', 'default')
    readonly_fields = ['id']


#
# #
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceExtendField, EextendFieldAdmin)
