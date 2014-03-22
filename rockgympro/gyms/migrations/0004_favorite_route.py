# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0003_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='route',
            field=models.ForeignKey(to='gyms.Route', to_field='slug'),
            preserve_default=True,
        ),
    ]
