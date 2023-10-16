from django.conf import settings


def after_account_create(data):
    """
    After Account Create Event & Webhook
    """
    # Event
    try:
        # Event Callback Function Provided In Project Settings File
        settings.ZF_EVENT_AFTER_ACCOUNT_CREATE(data)
    except:
        # Event Callback Function Not Provided In Project Settings File
        pass

    # Webhook
    try:
        # Webhook Settings Added
        is_webhook_enabled = settings.ZF_ENABLE_WEBHOOK
    except:
        # Webhook Settings Not Added
        pass


def after_form_create(data):
    """
    After Form Create Event & Webhook
    """
    # Event
    try:
        # Event Callback Function Provided In Project Settings File
        settings.ZF_EVENT_AFTER_FORM_CREATE(data)
    except:
        # Event Callback Function Not Provided In Project Settings File
        pass

    # Webhook
    try:
        # Webhook Settings Added
        is_webhook_enabled = settings.ZF_ENABLE_WEBHOOK
    except:
        # Webhook Settings Not Added
        pass


def after_form_submit(data):
    """
    After Form Submit Event & Webhook
    """
    # Event
    try:
        # Event Callback Function Provided In Project Settings File
        settings.ZF_EVENT_AFTER_FORM_SUBMIT(data)
    except:
        # Event Callback Function Not Provided In Project Settings File
        pass

    # Webhook
    try:
        # Webhook Settings Added
        is_webhook_enabled = settings.ZF_ENABLE_WEBHOOK
    except:
        # Webhook Settings Not Added
        pass