from django.db import models
from django.utils import timezone


# Create your models here.
class InvoiceType(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    invoice_type_code = models.CharField(verbose_name='发票类型状态码', max_length=128)
    invoice_type_value = models.CharField(verbose_name='发票类型状态名', max_length=128)
    description = models.CharField(verbose_name='描述', max_length=128)

    class Meta:
        db_table = 'invoice_type'
        verbose_name_plural = "发票-发票类型表"

    def __str__(self):
        return f"{self.id}"


class InvoiceStatus(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    invoice_status = models.CharField(verbose_name='发票状态码', max_length=128)
    invoice_status_value = models.CharField(verbose_name='发票状态名', max_length=128)
    description = models.CharField(verbose_name='描述', max_length=128)

    class Meta:
        db_table = 'invoice_status'
        verbose_name_plural = "发票-发票状态表"

    def __str__(self):
        return f"{self.id}"


class InvoiceExternalStatus(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    external_status_code = models.CharField(verbose_name='外经证状态码', max_length=128)
    external_status_value = models.CharField(verbose_name='外经证状态名', max_length=128)
    description = models.CharField(verbose_name='描述', max_length=128)

    class Meta:
        db_table = 'invoice_external_status'
        verbose_name_plural = "发票-外经证状态表"

    def __str__(self):
        return f"{self.id}"


class InvoiceToEnroll(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    invoice_id = models.IntegerField(verbose_name='发票id', primary_key=False, help_text='')
    enroll_id = models.IntegerField(verbose_name='报名id', primary_key=False, help_text='')

    class Meta:
        db_table = 'invoice_to_enroll'
        verbose_name_plural = "发票-映射"

    def __str__(self):
        return f"{self.id}"


class InvoiceExternal(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    thread_id = models.IntegerField(verbose_name='合同ID（信息id）', primary_key=False, help_text='')
    external_number = models.CharField(verbose_name='外经证编号', max_length=128, unique=True, blank=True, null=True,
                                       db_index=True,
                                       help_text='')
    external_price = models.DecimalField(verbose_name='开具金额', max_digits=32, decimal_places=2, blank=True,
                                         null=True)
    create_date = models.DateTimeField(verbose_name='开具日期', auto_now_add=True)
    tax_date = models.DateTimeField(verbose_name='税单日期', auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='结束日期', auto_now_add=True)
    external_address = models.CharField(verbose_name='外经证地址', max_length=128, blank=True, null=True, help_text='')
    remark = models.CharField(verbose_name='备注', max_length=128, blank=True, null=True, help_text='')
    external_status = models.ForeignKey(InvoiceExternalStatus, verbose_name='外经证状态', on_delete=models.DO_NOTHING,
                                        help_text='')
    return_date = models.DateTimeField(verbose_name='退回日期', auto_now_add=True)
    destroy_name = models.CharField(verbose_name='缴销作废状态', max_length=128, blank=True, null=True, help_text='')
    destroy_date = models.DateTimeField(verbose_name='缴销作废日期', auto_now_add=True)

    class Meta:
        db_table = 'invoice_external'
        verbose_name_plural = "发票-外经证表"

    def __str__(self):
        return f"{self.id}"


class InvoiceHeader(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    user_id = models.IntegerField(verbose_name='所属用户ID', primary_key=False, help_text='')
    head_type = models.CharField(verbose_name='抬头类型 PERSONS个人 CORPORATIONS企业', max_length=128, blank=True,
                                 null=False,
                                 help_text='')
    company_name = models.CharField(verbose_name='公司名称', max_length=128, blank=True, null=True,
                                    help_text='')
    tax_number = models.CharField(verbose_name='发票税号', max_length=128, unique=True, blank=True, null=True,
                                  db_index=True,
                                  help_text='')
    address = models.CharField(verbose_name='地址', max_length=128, blank=True, null=True, help_text='')
    account_opening_bank = models.CharField(verbose_name='开户行', max_length=128, blank=True, null=True, help_text='')
    account = models.CharField(verbose_name='账户', max_length=128, blank=True, null=True, help_text='')
    phone_number = models.CharField(verbose_name='手机号', max_length=128, blank=True, null=True, help_text='')
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, blank=True, null=True, )
    sort = models.IntegerField(verbose_name='排序', primary_key=False, help_text='', default=0, )

    class Meta:
        db_table = 'invoice_header'
        verbose_name_plural = "发票-抬头"

    def __str__(self):
        return f"{self.id}"


class Invoice(models.Model):
    """ 8、*invoice_invoice 发票表 """
    id = models.AutoField(verbose_name='平台ID', primary_key=True, help_text='必填。自动生成。')
    user_id = models.IntegerField(verbose_name='开票用户', primary_key=False, help_text='')
    thread_id = models.IntegerField(verbose_name='合同ID（信息id）', primary_key=False, help_text='')
    enroll_id_list = models.CharField(verbose_name='报名列表', max_length=128, blank=True, null=True,
                                      db_index=True,
                                      help_text='要开票的报名表数据')
    invoice_time = models.DateTimeField(verbose_name='开票时间', null=True)
    invoice_type = models.ForeignKey(InvoiceType, verbose_name='发票类型', on_delete=models.DO_NOTHING, help_text='')
    invoice_status = models.ForeignKey(InvoiceStatus, verbose_name='发票状态', on_delete=models.DO_NOTHING,
                                       help_text='', default=1)
    invoice_header = models.ForeignKey(InvoiceHeader, verbose_name='发票抬头', on_delete=models.DO_NOTHING,
                                       help_text='')

    invoice_number = models.CharField(verbose_name='发票号码', max_length=128, unique=True, blank=True, null=True,
                                      db_index=True,
                                      help_text='')
    invoice_price = models.DecimalField(verbose_name='开票金额', max_digits=32, decimal_places=2, blank=True, null=True)
    tax_rate = models.CharField(verbose_name='发票税率', max_length=128, blank=True, null=True, help_text='')
    invoice_tax = models.DecimalField(verbose_name='税额', max_digits=32, decimal_places=2, blank=True, null=True)
    invoice_untaxed = models.DecimalField(verbose_name='不含税金额', max_digits=32, decimal_places=2, blank=True,
                                          null=True)

    tax_number = models.CharField(verbose_name='税务登记号', max_length=128, blank=True, db_index=True, null=True,
                                  help_text='')

    operator_user_id = models.IntegerField(verbose_name='开票操作员', primary_key=False, help_text='')
    invoicing_party = models.CharField(verbose_name='开票方', max_length=128, blank=True, db_index=True, null=True,
                                       help_text='')
    remark = models.CharField(verbose_name='备注', max_length=128, blank=True, null=True, help_text='')
    destroy_name = models.CharField(verbose_name='退回作废状态', max_length=128, blank=True, null=True, help_text='')
    destroy_date = models.DateTimeField(verbose_name='退回作废日期', default=timezone.now, help_text='')
    destroy_reason = models.CharField(verbose_name='退回作废原因', max_length=128, blank=True, null=True, help_text='')
    destroy_operator_id = models.IntegerField(verbose_name='退回操作员', primary_key=False, help_text='')

    invoice_voucher = models.CharField(verbose_name='开票凭证', max_length=128, blank=True, null=True, help_text='')
    receive_email = models.EmailField(verbose_name='接收邮箱', unique=True, blank=True, help_text='')
    receive_phone = models.CharField(verbose_name='接收手机号', max_length=128, blank=True, null=True, help_text='')
    invoice_snapshot = models.JSONField(verbose_name='发票快照', blank=True, null=True, help_text='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=True)

    class Meta:
        db_table = 'invoice_invoice'
        verbose_name_plural = "01. 发票 - 发票表"

    def __str__(self):
        return f"{self.id}"


class InvoiceExtendData(models.Model):
    """ 5、invoice_extend_data扩展字段数据表 """

    class Meta:
        db_table = 'invoice_extend_data'
        verbose_name_plural = '发票- 扩展字段数据表'

    invoice_id = models.OneToOneField(verbose_name='发票ID', to=Invoice, related_name="invoice_extend_data",
                                      db_column='invoice_id',
                                      primary_key=True, on_delete=models.DO_NOTHING, help_text='')
    field_1 = models.CharField(verbose_name='自定义字段_1', max_length=255, blank=True, null=True, help_text='')
    field_2 = models.CharField(verbose_name='自定义字段_2', max_length=255, blank=True, null=True, help_text='')
    field_3 = models.CharField(verbose_name='自定义字段_3', max_length=255, blank=True, null=True, help_text='')
    field_4 = models.CharField(verbose_name='自定义字段_4', max_length=255, blank=True, null=True, help_text='')
    field_5 = models.CharField(verbose_name='自定义字段_5', max_length=255, blank=True, null=True, help_text='')
    field_6 = models.CharField(verbose_name='自定义字段_6', max_length=255, blank=True, null=True, help_text='')
    field_7 = models.CharField(verbose_name='自定义字段_7', max_length=255, blank=True, null=True, help_text='')
    field_8 = models.CharField(verbose_name='自定义字段_8', max_length=255, blank=True, null=True, help_text='')
    field_9 = models.CharField(verbose_name='自定义字段_9', max_length=255, blank=True, null=True, help_text='')
    field_10 = models.CharField(verbose_name='自定义字段_10', max_length=255, blank=True, null=True, help_text='')
    field_11 = models.CharField(verbose_name='自定义字段_11', max_length=255, blank=True, null=True, help_text='')
    field_12 = models.CharField(verbose_name='自定义字段_12', max_length=255, blank=True, null=True, help_text='')
    field_13 = models.CharField(verbose_name='自定义字段_13', max_length=255, blank=True, null=True, help_text='')
    field_14 = models.CharField(verbose_name='自定义字段_14', max_length=255, blank=True, null=True, help_text='')
    field_15 = models.CharField(verbose_name='自定义字段_15', max_length=255, blank=True, null=True, help_text='')
    field_16 = models.CharField(verbose_name='自定义字段_16', max_length=255, blank=True, null=True, help_text='')
    field_17 = models.CharField(verbose_name='自定义字段_17', max_length=255, blank=True, null=True, help_text='')
    field_18 = models.CharField(verbose_name='自定义字段_18', max_length=255, blank=True, null=True, help_text='')
    field_19 = models.CharField(verbose_name='自定义字段_19', max_length=255, blank=True, null=True, help_text='')
    field_20 = models.CharField(verbose_name='自定义字段_20', max_length=255, blank=True, null=True, help_text='')
    field_21 = models.CharField(verbose_name='自定义字段_21', max_length=255, blank=True, null=True, help_text='')
    field_22 = models.CharField(verbose_name='自定义字段_22', max_length=255, blank=True, null=True, help_text='')
    field_23 = models.CharField(verbose_name='自定义字段_23', max_length=255, blank=True, null=True, help_text='')
    field_24 = models.CharField(verbose_name='自定义字段_24', max_length=255, blank=True, null=True, help_text='')
    field_25 = models.CharField(verbose_name='自定义字段_25', max_length=255, blank=True, null=True, help_text='')
    field_26 = models.CharField(verbose_name='自定义字段_26', max_length=255, blank=True, null=True, help_text='')
    field_27 = models.CharField(verbose_name='自定义字段_27', max_length=255, blank=True, null=True, help_text='')
    field_28 = models.CharField(verbose_name='自定义字段_28', max_length=255, blank=True, null=True, help_text='')
    field_29 = models.CharField(verbose_name='自定义字段_29', max_length=255, blank=True, null=True, help_text='')
    field_30 = models.CharField(verbose_name='自定义字段_30', max_length=255, blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.invoice_id}"

    def short_field_1(self):
        if self.field_1 and len(self.field_1) > 25:
            return f"{self.field_1[0:25]}..."
        return self.field_1

    short_field_1.short_description = '自定义字段1'

    def short_field_2(self):
        if self.field_2 and len(self.field_2) > 25:
            return f"{self.field_2[0:25]}..."
        return self.field_2

    short_field_2.short_description = '自定义字段2'

    def short_field_3(self):
        if self.field_3 and len(self.field_3) > 25:
            return f"{self.field_3[0:25]}..."
        return self.field_3

    short_field_3.short_description = '自定义字段3'

    def short_field_4(self):
        if self.field_4 and len(self.field_4) > 25:
            return f"{self.field_4[0:25]}..."
        return self.field_4

    short_field_4.short_description = '自定义字段4'

    def short_field_5(self):
        if self.field_5 and len(self.field_5) > 25:
            return f"{self.field_5[0:25]}..."
        return self.field_5

    short_field_5.short_description = '自定义字段5'

    def short_field_6(self):
        if self.field_6 and len(self.field_6) > 25:
            return f"{self.field_6[0:25]}..."
        return self.field_6

    short_field_6.short_description = '自定义字段6'

    def short_field_7(self):
        if self.field_7 and len(self.field_7) > 25:
            return f"{self.field_7[0:25]}..."
        return self.field_7

    short_field_7.short_description = '自定义字段7'

    def short_field_8(self):
        if self.field_8 and len(self.field_8) > 25:
            return f"{self.field_8[0:25]}..."
        return self.field_8

    short_field_8.short_description = '自定义字段8'

    def short_field_9(self):
        if self.field_9 and len(self.field_9) > 25:
            return f"{self.field_9[0:25]}..."
        return self.field_9

    short_field_9.short_description = '自定义字段9'

    def short_field_10(self):
        if self.field_10 and len(self.field_10) > 25:
            return f"{self.field_10[0:25]}..."
        return self.field_10

    short_field_10.short_description = '自定义字段10'

    def short_field_11(self):
        if self.field_11 and len(self.field_11) > 25:
            return f"{self.field_11[0:25]}..."
        return self.field_11

    short_field_11.short_description = '自定义字段11'

    def short_field_12(self):
        if self.field_12 and len(self.field_12) > 25:
            return f"{self.field_12[0:25]}..."
        return self.field_12

    short_field_12.short_description = '自定义字段12'

    def short_field_13(self):
        if self.field_13 and len(self.field_13) > 25:
            return f"{self.field_13[0:25]}..."
        return self.field_13

    short_field_13.short_description = '自定义字段13'

    def short_field_14(self):
        if self.field_14 and len(self.field_14) > 25:
            return f"{self.field_14[0:25]}..."
        return self.field_14

    short_field_14.short_description = '自定义字段14'

    def short_field_15(self):
        if self.field_15 and len(self.field_15) > 25:
            return f"{self.field_15[0:25]}..."
        return self.field_15

    short_field_15.short_description = '自定义字段15'

    def short_field_16(self):
        if self.field_16 and len(self.field_16) > 25:
            return f"{self.field_16[0:25]}..."
        return self.field_16

    short_field_16.short_description = '自定义字段16'

    def short_field_17(self):
        if self.field_17 and len(self.field_17) > 25:
            return f"{self.field_17[0:25]}..."
        return self.field_17

    short_field_17.short_description = '自定义字段17'

    def short_field_18(self):
        if self.field_18 and len(self.field_18) > 25:
            return f"{self.field_18[0:25]}..."
        return self.field_18

    short_field_18.short_description = '自定义字段18'

    def short_field_19(self):
        if self.field_19 and len(self.field_19) > 25:
            return f"{self.field_19[0:25]}..."
        return self.field_19

    short_field_19.short_description = '自定义字段19'

    def short_field_20(self):
        if self.field_20 and len(self.field_20) > 25:
            return f"{self.field_20[0:25]}..."
        return self.field_20

    short_field_20.short_description = '自定义字段20'

    def short_field_21(self):
        if self.field_21 and len(self.field_21) > 25:
            return f"{self.field_21[0:25]}..."
        return self.field_21

    short_field_21.short_description = '自定义字段21'

    def short_field_22(self):
        if self.field_22 and len(self.field_22) > 25:
            return f"{self.field_22[0:25]}..."
        return self.field_22

    short_field_22.short_description = '自定义字段22'

    def short_field_23(self):
        if self.field_23 and len(self.field_23) > 25:
            return f"{self.field_23[0:25]}..."
        return self.field_23

    short_field_23.short_description = '自定义字段23'

    def short_field_24(self):
        if self.field_24 and len(self.field_24) > 25:
            return f"{self.field_24[0:25]}..."
        return self.field_24

    short_field_24.short_description = '自定义字段24'

    def short_field_25(self):
        if self.field_25 and len(self.field_25) > 25:
            return f"{self.field_25[0:25]}..."
        return self.field_25

    short_field_25.short_description = '自定义字段25'

    def short_field_26(self):
        if self.field_26 and len(self.field_26) > 25:
            return f"{self.field_26[0:25]}..."
        return self.field_26

    short_field_26.short_description = '自定义字段26'

    def short_field_27(self):
        if self.field_27 and len(self.field_27) > 25:
            return f"{self.field_27[0:25]}..."
        return self.field_27

    short_field_27.short_description = '自定义字段27'

    def short_field_28(self):
        if self.field_28 and len(self.field_28) > 25:
            return f"{self.field_28[0:25]}..."
        return self.field_28

    short_field_28.short_description = '自定义字段28'

    def short_field_29(self):
        if self.field_29 and len(self.field_29) > 25:
            return f"{self.field_29[0:25]}..."
        return self.field_29

    short_field_29.short_description = '自定义字段29'

    def short_field_30(self):
        if self.field_30 and len(self.field_30) > 25:
            return f"{self.field_30[0:25]}..."
        return self.field_30

    short_field_30.short_description = '自定义字段30'


# 扩展字段表。用于声明扩展字段数据表中的(有序)字段具体对应的什么键名。注意：扩展字段是对分类的扩展，而不是主类别的扩展
class InvoiceExtendField(models.Model):
    """  6、InvoiceExtendField 扩展字段表 """

    class Meta:
        db_table = 'invoice_extend_field'
        verbose_name_plural = '发票 - 扩展字段表'
        # ordering = ['-invoice_type_id']

    field_index_choices = [
        ("field_1", "field_1"),
        ("field_2", "field_2"),
        ("field_3", "field_3"),
        ("field_4", "field_4"),
        ("field_5", "field_5"),
        ("field_6", "field_6"),
        ("field_7", "field_7"),
        ("field_8", "field_8"),
        ("field_9", "field_9"),
        ("field_10", "field_10"),
        ("field_11", "field_11"),
        ("field_12", "field_12"),
        ("field_13", "field_13"),
        ("field_14", "field_14"),
        ("field_15", "field_15"),
        ("field_16", "field_16"),
        ("field_17", "field_17"),
        ("field_18", "field_18"),
        ("field_19", "field_19"),
        ("field_20", "field_20"),
        ("field_21", "field_21"),
        ("field_22", "field_22"),
        ("field_23", "field_23"),
        ("field_24", "field_24"),
        ("field_25", "field_25"),
        ("field_26", "field_26"),
        ("field_27", "field_27"),
        ("field_28", "field_28"),
        ("field_29", "field_29"),
        ("field_30", "field_30")
    ]
    type_choices = [
        ("string", "string"),
        ("int", "int"),
        ("float", "float"),
        ("bool", "bool"),
        ("select", "select"),
        ("radio", "radio"),
        ("checkbox", "checkbox"),
        ("date", "date",),
        ("time", "time",),
        ("datetime", "datetime"),
        ("moon", "moon"),
        ("year", "year"),
        ("color", "color"),
        ("file", "file"),
        ("image", "image"),
        ("switch", "switch"),
        ("cascader", "cascader"),
        ("plain", "plain"),
        ("textarea", "textarea"),
        ("text", "text"),
        ("number", "number"),
        ("upload", "upload"),
        ("password", "password"),
    ]

    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    # 数据库生成classify_id字段
    # invoice_type = models.ForeignKey(verbose_name='发票ID', null=True, blank=True, to=InvoiceType,
    #                                  db_column='invoice_type_id', related_name='+', on_delete=models.DO_NOTHING,
    #                                  help_text='')
    field = models.CharField(verbose_name='自定义字段', max_length=255, help_text='')  # 眏射ThreadExtendData表的键名
    field_index = models.CharField(verbose_name='冗余字段', max_length=255, help_text='',
                                   choices=field_index_choices)  # 眏射ThreadExtendData表的键名
    value = models.CharField(verbose_name='字段介绍', max_length=255, null=True, blank=True, help_text='')
    type = models.CharField(verbose_name='字段类型', max_length=255, blank=True, null=True, choices=type_choices,
                            help_text='')
    unit = models.CharField(verbose_name='参数单位', max_length=255, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='字段配置', blank=True, null=True, default=dict, help_text='')
    description = models.CharField(verbose_name='数据配置', max_length=255, blank=True, null=True, default=dict,
                                   help_text='')
    default = models.CharField(verbose_name='默认值', max_length=2048, blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.id}"
