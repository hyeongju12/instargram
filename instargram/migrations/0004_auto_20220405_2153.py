# Generated by Django 3.0.14 on 2022-04-05 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instargram', '0003_auto_20220405_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_user_set',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_post_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
