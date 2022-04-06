from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import resolve_url
from django.template.loader import render_to_string


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male" # "DB에 저장되는 값", "보여지는 값"
        FEMAILE = "F", "Female"
    #유저 팔로우를 위한 필드
    follower_set = models.ManyToManyField('self', blank=True)
    following_set = models.ManyToManyField('self', blank=True)

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r'^010-?[1-9]\d{3}-?\d{4}$')])
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)
    avatar = models.ImageField(blank=True, upload_to="accounts/profile/%Y/%m/%d",
                               help_text="45px * 45px 크기의 png/jpg 파일을 업로드 하세요.")

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)

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