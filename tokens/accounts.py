from django.db.models import Sum

from . import models


def create_account():
    """
    Creates a new account.

    :returns: Returns the new account.
    """
    return models.Account.objects.create()


def calculate_account_balance(account):
    """
    Calculates the account balance.

    :param account: The account of interest.
    :returns: Returns the account balance.
    """
    return models.Transaction.filter(
        account=account,
    ).order_by(
        'executed_on',
    ).aggregate(
        Sum('amount'),
    )
