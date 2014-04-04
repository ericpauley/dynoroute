# encoding: utf8
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0010_auto_20140403_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='color3',
            field=models.CharField(default='#ffffff', max_length=7, choices=[('#ffffff', 'Clear'), ('#d11f2d', 'Red'), ('#fef102', 'Yellow'), ('#FF6500', 'Orange'), ('#ed7696', 'Pink'), ('#6f3728', 'Dark Brown'), ('#bd955a', 'Light Brown'), ('#00b2e2', 'Light Blue'), ('#094080', 'Dark Blue'), ('#01b703', 'Lime Green'), ('#f2f2f2', 'White'), ('#009ca8', 'Teal'), ('#007a41', 'Dark Green'), ('#000000', 'Black'), ('#724c9f', 'Purple')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gym',
            name='tape_colors',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='date_set',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
