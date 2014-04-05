# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gyms', '0014_auto_20140405_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteFlag',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('route', models.ForeignKey(to='gyms.Route', to_field='slug')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('active', models.BooleanField(default=True)),
                ('message', models.TextField()),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
