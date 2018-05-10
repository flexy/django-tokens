from django.db import models
from django.conf import settings

from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import (
    TimeFramedModel,
    TimeStampedModel,
    StatusModel,
)
from djmoney.models.fields import MoneyField


class TokenType(TimeStampedModel):
    name = models.CharField(
        max_length=100,
    )
    value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
    )

    icon_front = models.ImageField()
    icon_back = models.ImageField()


class TokenTypeGroup(models.Model):
    name = models.CharField(
        max_length=100,
    )
    name_short = models.CharField(
        max_length=3,
    )
    token_types = models.ManyToManyField(
        TokenType,
    )

    icon = models.ImageField()


class Account(models.Model):
    pass


class Transaction(TimeStampedModel, StatusModel):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
    )
    token_type = models.ForeignKey(
        TokenType,
        on_delete=models.PROTECT,
    )

    amount = models.IntegerField()
    details = models.TextField(
        null=True,
        blank=True,
    )

    STATUS = Choices(
        'queued',
        'completed',
        'declined',
    )
    executed_on = models.DateTimeField(
        null=True,
        blank=True,
    )
    DECLINE_ERRORS = Choices(
        'insufficient_balance',
        'invalid_account',
    )
    decline_error = StatusField(
        choices_name='DECLINE_ERRORS',
        null=True,
        blank=True,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    @property
    def type(self):
        """
        :returns: Returns the transaction type.
        """
        if self.amount >= 0:
            return 'credit'
        elif self.amount < 0:
            return 'debit'

    def __str__(self):
        return '{} {} - Account: {}'.format(
            self.amount,
            self.type,
            self.account,
        )


class TransactionGroup(models.Model):
    transactions = models.ManyToManyField(
        Transaction,
    )

    TYPES = Choices(
        'refund',
        'transfer',
    )
    type = StatusField(
        choices_name='TYPES',
    )


class Hold(
    TimeFramedModel,
    TimeStampedModel,
    StatusModel,
):
    STATUS = Choices(
        'active',
        'cancelled',
        'released',
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
    )
    token_type = models.ForeignKey(
        TokenType,
        on_delete=models.PROTECT,
    )

    amount = models.PositiveIntegerField()
    details = models.TextField(
        null=True,
        blank=True,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
