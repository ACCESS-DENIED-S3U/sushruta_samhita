# django imports
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.conf import settings


def send_review_email(username, email, data):

    context = {
        'username': username,
        'email': email,
        'data': data,
    }

    email_subject = 'Quick mail from Sushruta Samhita for your health and wealth'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)