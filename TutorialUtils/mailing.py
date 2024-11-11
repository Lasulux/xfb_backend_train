# 1. Python standard library
from os import environ

# 2. Third party packages
from django.core import mail
from django.conf import settings

# 3. Own packages


def AddAttachments(email, attachments):
    if attachments:
        for a in attachments:
            email.attach(a["file_name"], a["file_content"], a["mime_type"])
    return email


def send_email(subject, message, recipient_list_name, attachments=None, from_email="hello@xfbanalytics.hu"):
    """Send email

    Args:
        subject (_type_): Subject of the email
        message (_type_): Message of the email
        recipient_list_name (_type_): List of recipients
        attachments (_type_, optional): Attachments list of dict. Defaults to None.
        from_email (str, optional): From email. Defaults to "hello@xfbanalytics.hu".

    Returns:
        _type_: _description_
    """
    recipient_list = environ.get(recipient_list_name).split(";")
    # Sending email using the primary Django email settings
    try:
        email = mail.EmailMessage(
            subject=subject, body=message, from_email=from_email, to=recipient_list, connection=None
        )
        email = AddAttachments(email=email, attachments=attachments)
        email.send(fail_silently=False)
    except:
        # If the primary provider does not work we define a new connection to Gmail
        connection = mail.get_connection()
        connection.port = settings.EMAIL_PORT
        connection.use_tls = settings.EMAIL_USE_TLS
        connection.host = settings.EMAIL_HOST_GOOGLE
        connection.username = settings.EMAIL_HOST_USER_GOOGLE
        connection.password = settings.EMAIL_HOST_PASSWORD_GOOGLE
        new_subject = f"<Message from: {from_email} > {subject}"
        email = mail.EmailMessage(
            subject=new_subject, body=message, from_email=from_email, to=recipient_list, connection=None
        )
        email = AddAttachments(email=email, attachments=attachments)
        email.send(fail_silently=False)
    return None
