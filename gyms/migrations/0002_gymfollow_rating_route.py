# encoding: utf8
from django.db import models, migrations
import datetime
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GymFollow',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('gym', models.ForeignKey(to='gyms.Gym', to_field=u'id')),
            ],
            options={
                u'unique_together': set([('gym', 'user')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('score', models.IntegerField()),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(primary_key=True, serialize=False, editable=False, blank=True, unique=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('type', models.CharField(default='bouldering', max_length=16, choices=[('top_rope', 'Top Rope'), ('bouldering', 'Bouldering')])),
                ('grade', models.DecimalField(max_digits=10, decimal_places=2, choices=[('Top Rope', [(Decimal('5'), '5.5'), (Decimal('6'), '5.6'), (Decimal('7'), '5.7'), (Decimal('8'), '5.8'), (Decimal('9'), '5.9'), (Decimal('9.25'), '5.9+'), (Decimal('9.75'), '5.10-'), (Decimal('10'), '5.10'), (Decimal('10.25'), '5.10+'), (Decimal('10.75'), '5.11-'), (Decimal('11'), '5.11'), (Decimal('11.25'), '5.11+'), (Decimal('11.75'), '5.12-'), (Decimal('12'), '5.12'), (Decimal('12.25'), '5.12+'), (Decimal('12.75'), '5.13-'), (Decimal('13'), '5.13'), (Decimal('13.25'), '5.13+'), (Decimal('13.75'), '5.14-'), (Decimal('14'), '5.14'), (Decimal('14.25'), '5.14+'), (Decimal('14.75'), '5.15-'), (Decimal('15'), '5.15'), (Decimal('15.25'), '5.15+')]), ('Bouldering', [(Decimal('999.75'), 'V0-'), (Decimal('1000'), 'V0'), (Decimal('1000.25'), 'V0+'), (Decimal('1000.75'), 'V1-'), (Decimal('1001'), 'V1'), (Decimal('1001.25'), 'V1+'), (Decimal('1001.75'), 'V2-'), (Decimal('1002'), 'V2'), (Decimal('1002.25'), 'V2+'), (Decimal('1002.75'), 'V3-'), (Decimal('1003'), 'V3'), (Decimal('1003.25'), 'V3+'), (Decimal('1003.75'), 'V4-'), (Decimal('1004'), 'V4'), (Decimal('1004.25'), 'V4+'), (Decimal('1004.75'), 'V5-'), (Decimal('1005'), 'V5'), (Decimal('1005.25'), 'V5+'), (Decimal('1005.75'), 'V6-'), (Decimal('1006'), 'V6'), (Decimal('1006.25'), 'V6+'), (Decimal('1006.75'), 'V7-'), (Decimal('1007'), 'V7'), (Decimal('1007.25'), 'V7+'), (Decimal('1007.75'), 'V8-'), (Decimal('1008'), 'V8'), (Decimal('1008.25'), 'V8+'), (Decimal('1008.75'), 'V9-'), (Decimal('1009'), 'V9'), (Decimal('1009.25'), 'V9+'), (Decimal('1009.75'), 'V10-'), (Decimal('1010'), 'V10'), (Decimal('1010.25'), 'V10+'), (Decimal('1010.75'), 'V11-'), (Decimal('1011'), 'V11'), (Decimal('1011.25'), 'V11+'), (Decimal('1011.75'), 'V12-'), (Decimal('1012'), 'V12'), (Decimal('1012.25'), 'V12+'), (Decimal('1012.75'), 'V13-'), (Decimal('1013'), 'V13'), (Decimal('1013.25'), 'V13+')])])),
                ('setter', models.ForeignKey(to_field=u'id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('location', models.CharField(max_length=32)),
                ('date_set', models.DateField(default=datetime.date(2014, 3, 22))),
                ('date_torn', models.DateField(null=True, blank=True)),
                ('gym', models.ForeignKey(to='gyms.Gym', to_field=u'id')),
                ('notes', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='route_images', blank=True)),
                ('views', models.IntegerField(default=0)),
                ('status', models.CharField(default='complete', max_length=16, choices=[('complete', 'Complete'), ('in_progress', 'In Progress'), ('not_started', 'Not Started')])),
                ('color1', models.CharField(default='#ffffff', max_length=7, choices=[('#ffffff', 'Clear'), ('#d11f2d', 'Red'), ('#fef102', 'Yellow'), ('#FF6500', 'Orange'), ('#ed7696', 'Pink'), ('#6f3728', 'Dark Brown'), ('#bd955a', 'Light Brown'), ('#00b2e2', 'Light Blue'), ('#094080', 'Dark Blue'), ('#01b703', 'Lime Green'), ('#f2f2f2', 'White'), ('#009ca8', 'Teal'), ('#007a41', 'Dark Green'), ('#000000', 'Black'), ('#724c9f', 'Purple')])),
                ('color2', models.CharField(default='#ffffff', max_length=7, choices=[('#ffffff', 'Clear'), ('#d11f2d', 'Red'), ('#fef102', 'Yellow'), ('#FF6500', 'Orange'), ('#ed7696', 'Pink'), ('#6f3728', 'Dark Brown'), ('#bd955a', 'Light Brown'), ('#00b2e2', 'Light Blue'), ('#094080', 'Dark Blue'), ('#01b703', 'Lime Green'), ('#f2f2f2', 'White'), ('#009ca8', 'Teal'), ('#007a41', 'Dark Green'), ('#000000', 'Black'), ('#724c9f', 'Purple')])),
                ('favorites', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='gyms.Favorite')),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
