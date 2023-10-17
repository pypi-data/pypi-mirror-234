# encoding: utf-8
"""
@project: djangoModel->extend_service
@author:高栋天
@Email: sky4834@163.com
@synopsis: 扩展服务
@created_time: 2022/7/29 15:14
"""
from django.db.models import F

from ..models import *
from ..utils.custom_tool import write_to_log, force_transform_type, filter_result_field, format_params_handle


# 扩展字段增删改查
class InvoiceExtendService:
    @staticmethod
    def create_or_update(params=None, invoice_id=None, invoice_type_id=None, **kwargs):
        """
        信息表扩展信息新增或者修改
        :param params: 扩展信息，必填
        :param invoice_id: 发票ID，必填
        :param invoice_type_id: 沙盒ID, 非必填
        :return: None，err
        """
        # 参数合并，强制类型转换
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)
        # 不存在信息ID 无法修改
        invoice_id = invoice_id or params.pop("invoice_id", None)
        invoice_id, is_void = force_transform_type(variable=invoice_id, var_type="int")
        if invoice_id is None:
            return None, "扩展字段修改错误,invoice_id不可以为空"
        # 检查信息ID 是否正确
        invoice_obj = Invoice.objects.filter(id=invoice_id).first()
        if not invoice_obj:
            return None, "没有找到该主表信息，无法添加扩展信息"
        # 扩展字段映射, 如没有配置对应类别的扩展字段，则无法添加扩展数据。
        extend_fields = InvoiceExtendField.objects.values("field_index",
                                                          "default",
                                                          "field")
        if not extend_fields:
            return None, "没有配置扩展字段，无法添加扩展信息"

        extend_model_fields = [i.name for i in InvoiceExtendData._meta.fields if
                               not i.name == "invoice_id"]  # 扩展信息表的字段列表
        # 扩展数据替换
        extend_field_map = {item["field"]: item["field_index"] for item in extend_fields if
                            item["field_index"] in extend_model_fields}  # 得到合理的配置
        transformed_extend_params = {extend_field_map[k]: v for k, v in params.items() if
                                     extend_field_map.get(k)}  # {"自定义扩展字段":"123"} ==>> {"filed_1":"123"}
        # 修改或添加数据
        try:
            extend_obj = InvoiceExtendData.objects.filter(invoice_id=invoice_id)
            if not extend_obj:
                # 新增的时候，启用扩展字段参数设置默认值。
                # 注意：防止后台管理员配置错误,出现数据表不存在的字段。所以需要进行一次字段排除
                default_field_map = {item["field_index"]: item["default"] for item in extend_fields if
                                     (item["default"] and item["field_index"] in extend_model_fields)}
                for field_index, default in default_field_map.items():
                    transformed_extend_params.setdefault(field_index, default)
                if not transformed_extend_params:
                    return None, "没有可添加的数据，请检查扩展字段的默认值配置"

                # 添加扩展信息
                transformed_extend_params.setdefault('invoice_id_id', invoice_id)
                InvoiceExtendData.objects.create(**transformed_extend_params)
                return None, None
            else:
                if not transformed_extend_params:
                    return None, "没有可修改的数据"

                extend_obj.update(**transformed_extend_params)
                return None, None
        except Exception as e:
            write_to_log(prefix="信息表扩展信息新增或者修改异常", err_obj=e)
            return None, "信息表扩展信息新增或者修改异常:" + str(e)

    @staticmethod
    def get_extend_info(invoice_id_list: list = None):
        """
        获取映射后的扩展数据
        :param invoice_id_list: 发票ID列表
        :return: extend_list, err
        """
        # 参数类型校验
        invoice_id_list, is_void = force_transform_type(variable=invoice_id_list, var_type="list")
        if not invoice_id_list:
            return [], None

        # 扩展字段映射, 如没有配置对应类别的扩展字段，则无法添加扩展数据。
        extend_fields = list(InvoiceExtendField.objects.values("field_index", "field"))
        if not extend_fields:
            return [], None
        extend_field_map = {}
        for item in extend_fields:
            extend_field_map.update({item["field_index"]: item["field"]})
        # 查询出扩展原始数据
        try:
            invoice_extend_list = list(InvoiceExtendData.objects.filter(invoice_id__in=invoice_id_list).values())
        except Exception as e:
            return [], "获取扩展数据异常"
        # 处理获取到结果，字段替换
        try:
            finish_list = []
            for i in invoice_extend_list:
                # 进行替换
                finish_list.append(format_params_handle(
                    param_dict=i,
                    alias_dict=extend_field_map,
                    is_remove_null=False
                ))
            # 剔除不需要的字段
            finish_list = filter_result_field(
                result_list=finish_list,
                remove_filed_list=[i.name for i in InvoiceExtendData._meta.fields if not i.name == "invoice_id"]
            )
            return finish_list, None

        except Exception as e:
            write_to_log(prefix="获取映射后的扩展数据,数据拼接异常", err_obj=e,
                         content="invoice_id_list:" + str(invoice_id_list))
            return [], None
