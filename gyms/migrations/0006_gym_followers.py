# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gyms', '0005_favorite_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='followers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='gyms.GymFollow'),
            preserve_default=True,
        ),
    ]
