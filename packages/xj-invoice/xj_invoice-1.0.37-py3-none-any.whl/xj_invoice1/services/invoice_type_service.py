import sys
import time
import os
import datetime

from ..models import *


class InvoiceTypeService:

    @staticmethod
    def list():
        invoice_type = InvoiceType.objects.values("id", "invoice_type_code", "invoice_type_value", "description")
        return list(invoice_type), None
