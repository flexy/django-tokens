from django.contrib import admin

from . import models


admin.site.register(models.TokenType)
admin.site.register(models.Account)
admin.site.register(models.Transaction)
admin.site.register(models.TransactionGroup)
