# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0012_auto_20140403_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='top_rope_format',
            field=models.CharField(default='yds_plusminus', max_length=16, choices=[('yds_abcd', 'YDS ABCD'), ('yds_plusminus', 'YDS +/-'), ('french', 'French')]),
        ),
        migrations.AlterField(
            model_name='gym',
            name='lead_format',
            field=models.CharField(default='yds_plusminus', max_length=16, choices=[('yds_abcd', 'YDS ABCD'), ('yds_plusminus', 'YDS +/-'), ('french', 'French')]),
        ),
        migrations.AlterField(
            model_name='gym',
            name='bouldering_format',
            field=models.CharField(default='hueco', max_length=16, choices=[('hueco', 'Hueco'), ('riao', 'RIAO'), ('font', 'Font')]),
        ),
    ]
