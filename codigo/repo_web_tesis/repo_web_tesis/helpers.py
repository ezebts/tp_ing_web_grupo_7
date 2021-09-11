from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email(destination_emails, subject, template, context={}):
    template = get_template(template)

    print("CTX: ", context)

    content = template.render(context)

    message = EmailMultiAlternatives(
        subject, "''", settings.EMAIL_HOST_USER, destination_emails)

    message.attach_alternative(content, 'text/html')

    message.content_subtype = 'text/html'

    print("EMAIL: ", content)

    message.send()
