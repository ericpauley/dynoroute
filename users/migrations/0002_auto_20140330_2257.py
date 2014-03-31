# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.IntegerField(blank=True, null=True, choices=[(10000, 'Owner'), (5000, 'Manager'), (1000, 'Setter'), (500, 'Employee'), (900, 'Head Coach')]),
        ),
    ]
