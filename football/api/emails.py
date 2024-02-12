from django.core.mail import send_mail
from django.conf import settings

def send_token_via_email(email,token):
    subject = 'Login verification email'
    message = f'Your token is {token} '
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])