# encoding: utf8
from django.db import models, migrations
import datetime
import gyms.models


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0008_route_sends'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='address',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gym',
            name='desc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gym',
            name='image',
            field=models.ImageField(null=True, upload_to=gyms.models.about_image_upload, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gym',
            name='phone',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gym',
            name='logo',
            field=models.ImageField(upload_to=gyms.models.logo_upload, blank=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='image',
            field=models.ImageField(upload_to=gyms.models.get_image_name, blank=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='date_set',
            field=models.DateField(default=datetime.date(2014, 3, 30)),
        ),
        migrations.AlterField(
            model_name='route',
            name='status',
            field=models.CharField(default='complete', max_length=16, choices=[('complete', 'Complete'), ('in_progress', 'In Progress'), ('not_started', 'Not Started'), ('torn', 'Torn')]),
        ),
    ]
