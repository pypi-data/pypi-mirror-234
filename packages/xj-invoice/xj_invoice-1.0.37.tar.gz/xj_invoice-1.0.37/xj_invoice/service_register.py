# encoding: utf-8
"""
@project: djangoModel->service_register
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 对外开放服务调用注册白名单
@created_time: 2023/1/12 14:29
"""

import xj_invoice
from xj_invoice.services import invoice_service

# 对外服务白名单
register_list = [
    {
        # 发票流程写入
        "service_name": "invoice_add",
        "pointer": invoice_service.InvoiceService.add
    },

]


# 遍历注册
def register():
    for i in register_list:
        setattr(xj_invoice, i["service_name"], i["pointer"])


if __name__ == '__main__':
    register()
