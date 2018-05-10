from . import models, utils


def credit(amount, *args, **kwargs):
    """
    Creates a credit transaction.

    :param amount: The absolute value of the amount to be credited.
    :returns: Returns the credit transaction.
    """
    create_transaction(
        amount,
        *args,
        **kwargs
    )


def debit(amount, *args, **kwargs):
    """
    Creates a debit transaction.

    :param amount: The absolute value of the amount to be debited.
    :returns: Returns the debit transaction.
    """
    amount = -amount
    return create_transaction(
        amount,
        *args,
        **kwargs
    )


def refund(
    transaction,
    creator,
    reason=None,
    amount=None,
):
    """
    Refunds a transaction.

    :param transaction: The transaction on which to base the refund.
    :param creator: The user that created the refund transaction.
    :param reason: If not ``None``, the reason for the refund.
    :param amount: If not ``None``, refund this amount rather than the whole
        transaction.
    :returns: Returns the refund transaction.
    """
    # Calculate the amount to be refunded
    if not amount:
        amount = transaction.amount

    # Parse the details
    reason_message = utils.create_reason_message(reason)
    details = utils.create_message_from_template(
        'refund',
        transaction.id,
        amount,
        reason_message,
    )

    # Create the refund transaction
    refund_transaction = create_transaction(
        amount,
        transaction.token_type,
        transaction.account,
        creator,
        details=details,
    )

    # Relate the refund transaction to the original transaction
    transaction_group = models.TransactionGroup(
        type='refund',
    )
    transaction_group.transaction_set.set([
        transaction,
        refund_transaction,
    ])
    transaction_group.save()

    # Return the new transaction
    return refund_transaction


def transfer(
    amount,
    token_type,
    account1,
    account2,
    creator,
    reason=None,
):
    """
    Transfers from one account to another.

    :param amount: The amount of the transfer.
    :param token_type: The type of token to be transferred.
    :param account1: The account from which the amount will be taken.
    :param account2: The account which will receive the amount.
    :param creator: The user that created the transaction.
    :param reason: If not ``None``, the reason for the transfer.
    :returns: Returns the transfer transaction group.
    """
    # Parse the details
    reason_message = utils.create_reason_message(reason)
    debit_details = utils.create_message_from_template(
        'transfer_debit',
        amount,
        account2,
        reason_message,
    )
    credit_details = utils.create_message_from_template(
        'transfer_credit',
        amount,
        account1,
        reason_message,
    )

    # Create a debit on the first account
    debit_transaction = debit(
        amount,
        token_type,
        account1,
        creator,
        details=debit_details,
    )

    # Create a credit on the second account
    credit_transaction = credit(
        amount,
        token_type,
        account2,
        creator,
        details=credit_details,
    )

    # Relate the transactions
    transaction_group = models.TransactionGroup(
        type='transfer',
    )
    transaction_group.transaction_set.set([
        debit_transaction,
        credit_transaction,
    ])
    transaction_group.save()

    # Return the transaction group
    return transaction_group


def create_transaction(
    amount,
    token_type,
    account,
    creator,
    **kwargs
):
    """
    Creates a new transaction.

    :param amount: The amount of the transaction. This is positive for credit
        and negative for debit.
    :param token_type: The type of token for the transaction.
    :param account: The account to which the transaction should be applied.
    :param creator: The user that created the transaction.
    :returns: Returns the transaction.
    """
    return models.Transaction.create(
        account=account,
        token_type=token_type,
        amount=amount,
        creator=creator,

        # Assumed fields
        status='queued',

        # Additional fields
        **kwargs
    )


def create_hold(
    amount,
    token_type,
    account,
    creator,
    **kwargs
):
    """
    Creates a hold.

    :param amount: The amount of the hold.
    :param token_type: The type of token for the hold.
    :param account: The account to which the hold should be applied.
    :param creator: The user that created the hold.
    :returns: Returns the hold.
    """
    return models.Hold.create(
        account=account,
        token_type=token_type,
        amount=amount,
        creator=creator,

        # Assumed fields
        status='active',

        # Additional fields
        **kwargs
    )


def release_hold(
    hold,
):
    """
    Releases a hold.

    :param hold: The hold to be released
    :returns: Returns the hold.
    """
    hold.status = 'released'
    hold.save()

    return hold
