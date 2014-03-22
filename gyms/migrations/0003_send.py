# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gyms', '0002_gymfollow_rating_route'),
    ]

    operations = [
        migrations.CreateModel(
            name='Send',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('route', models.ForeignKey(to='gyms.Route', to_field='slug')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
