# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0011_auto_20140403_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='tape_colors',
            field=models.IntegerField(default=2, choices=[(1, 1), (2, 2), (3, 3)]),
        ),
    ]
