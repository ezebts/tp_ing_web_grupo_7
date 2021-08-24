from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, reverse
from django.template.loader import get_template


def redirect_to(path):

    def redirection(request):
        return redirect(reverse(path))

    return redirection


def send_email(destination_emails, subject, template, context={}):
    template = get_template(template)

    content = template.render(context)

    message = EmailMultiAlternatives(
        subject, "''", settings.EMAIL_HOST_USER, destination_emails)

    message.attach_alternative(content, 'text/html')

    message.send()
