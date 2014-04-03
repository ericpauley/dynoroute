# encoding: utf8
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0009_auto_20140330_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='lead_format',
            field=models.CharField(default='yds_plusminus', max_length=16, choices=[('yds_abcd', 'YDS ABCD'), ('yds_plusminus', 'YDS +/-')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gym',
            name='bouldering_format',
            field=models.CharField(default='hueco', max_length=16, choices=[('hueco', 'Hueco'), ('riao', 'RIAO')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gym',
            name='top_rope_format',
            field=models.CharField(default='yds_plusminus', max_length=16, choices=[('yds_abcd', 'YDS ABCD'), ('yds_plusminus', 'YDS +/-')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='type',
            field=models.CharField(default='bouldering', max_length=16, choices=[('top_rope', 'Top Rope'), ('bouldering', 'Bouldering'), ('lead', 'Lead')]),
        ),
        migrations.AlterField(
            model_name='route',
            name='grade',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='route',
            name='date_set',
            field=models.DateField(default=datetime.date(2014, 4, 3)),
        ),
    ]
