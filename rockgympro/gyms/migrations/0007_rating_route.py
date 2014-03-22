# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0006_gym_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='route',
            field=models.ForeignKey(to='gyms.Route', to_field='slug'),
            preserve_default=True,
        ),
    ]
