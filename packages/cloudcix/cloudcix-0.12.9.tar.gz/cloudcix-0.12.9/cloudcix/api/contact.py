from cloudcix.client import Client


class Contact:
    """
    Contact Application will replace the Contacts Application

    The Contact Application is a CRM application that exposes a REST API to manage a shared address book between Users
    in the same Member.

    It is also a management system for the management of your CloudCIX Chatbots

    Contact can be used as a sales and marketing tool or just as a general purpose address book.
    """
    _application_name = 'Contact'

    activity = Client(
        _application_name,
        'activity_type/{activity_type_id}/activity/',
    )
    activity_type = Client(
        _application_name,
        'activity_type/',
    )
    auth = Client(
        _application_name,
        '{chatbot_name}/auth/',
    )
    campaign = Client(
        _application_name,
        'campaign/',
    )
    campaign_activity = Client(
        _application_name,
        'campaign/{campaign_id}/activity/',
    )
    campaign_contact = Client(
        _application_name,
        'campaign/{campaign_id}/contact/',
    )
    chatbot = Client(
        _application_name,
        'chatbot/',
    )
    contact = Client(
        _application_name,
        'contact/',
    )
    conversation = Client(
        _application_name,
        '{chatbot_name}/conversation/',
    )
    corpus = Client(
        _application_name,
        'chatbot/{chatbot_id}/corpus/',
    )
    group = Client(
        _application_name,
        'group/',
    )
    group_contact = Client(
        _application_name,
        'group/{group_id}/contact/',
    )
    opportunity = Client(
        _application_name,
        'opportunity/',
    )
    opportunity_contact = Client(
        _application_name,
        'opportunity/{opportunity_id}/contact/',
    )
    opportunity_history = Client(
        _application_name,
        'cpportunity/{opportunity_id}/history/',
    )
    q_and_a = Client(
        _application_name,
        '{chatbot_name}/conversation/{conversation_id}/q_and_a/',
    )
