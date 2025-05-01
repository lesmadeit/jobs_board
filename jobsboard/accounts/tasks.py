from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.token import account_activation_token
from django.contrib.auth import get_user_model

@shared_task(bind=True, reject_on_worker_lost=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True,retry_kwargs={'max_retries': 5})
def send_activation_email(self, user_id, domain, to_email):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        subject = 'Please activate your account'
        message = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(subject, message, to=[to_email])
        email.content_subtype = 'html'
        email.send()
    except:
        self.retry




@shared_task(bind=True, reject_on_worker_lost=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True,retry_kwargs={'max_retries': 5})
def send_password_reset_email(self, user_id, domain, to_email, email_template_name, subject_template_name):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        subject = render_to_string(subject_template_name).strip()
        message = render_to_string(email_template_name, {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(subject, message, to=[to_email])
        email.content_subtype = 'html'
        email.send()
    except:
        self.retry
        