# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0013_auto_20140405_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='phone',
            field=models.CharField(max_length=255, null=True, verbose_name='Phone Number', blank=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='desc',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
    ]
