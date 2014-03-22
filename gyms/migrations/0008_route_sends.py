# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gyms', '0007_rating_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='sends',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='gyms.Send'),
            preserve_default=True,
        ),
    ]
