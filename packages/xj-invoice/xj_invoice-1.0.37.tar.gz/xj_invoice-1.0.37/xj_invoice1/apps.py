from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xj_invoice'
    verbose_name = '发票系统'
    sort = 4
