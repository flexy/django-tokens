def create_message_from_template(template, *args, **kwargs):
    """
    Creates a message from a template.

    :param template: Reference to desired message template.
    :param *args: Variables to insert into the message template.
    :param **kwargs: Named variables to insert into the message template.
    :returns: Returns the message.
    """
    messages = {
        'reason': 'Reason: {}',
        'refund': 'Refunds transaction #{} to the amount of {}. {}',
        'transfer_debit': 'Send {} to account {}. {}',
        'transfer_credit': 'Receive {} from account {}. {}',
    }

    return messages[template].format(*args, **kwargs)


def create_reason_message(reason=None):
    """
    Creates a reason message.

    :param reason: Primary content of the message.
    :returns: Returns the message or an empty string if no reason is provided.
    """
    if reason:
        reason_message = create_message_from_template(
            'reason',
            reason,
        )
    else:
        reason_message = ''

    return reason_message
