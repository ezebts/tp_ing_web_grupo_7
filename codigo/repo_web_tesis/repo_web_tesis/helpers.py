from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def render_template(template_name, context={}):
    template = get_template(template_name)

    if template:
        return template.render(context)

    return None


def send_email(destination_emails, subject, template, context={}):
    content = render_template(template, context=context)

    message = EmailMultiAlternatives(
        subject, "''", settings.EMAIL_HOST_USER, destination_emails)

    message.attach_alternative(content, 'text/html')

    message.content_subtype = 'text/html'

    message.send()
