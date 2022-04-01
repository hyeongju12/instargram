from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    #post_save 시그널을 통해 사용자가 가입이되면 이메일 발송


    #django render to string
    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt", {
            "user" : self
        })
        content = render_to_string("accounts/welcome_email_content.txt", {
            "user" : self
        })
        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)