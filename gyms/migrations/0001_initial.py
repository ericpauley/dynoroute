# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=32)),
                ('location_options', models.TextField(blank=True)),
                ('named_routes', models.BooleanField(default=False)),
                ('logo', models.ImageField(upload_to='gym_images', blank=True)),
                ('website_url', models.URLField(blank=True)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
