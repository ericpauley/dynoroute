# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
        ('gyms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name=u'password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name=u'last login')),
                ('is_superuser', models.BooleanField(default=False, help_text=u'Designates that this user has all permissions without explicitly assigning them.', verbose_name=u'superuser status')),
                ('username', models.CharField(help_text=u'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, verbose_name=u'username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', u'Enter a valid username.', 'invalid')])),
                ('name', models.CharField(max_length=30, verbose_name=u'first name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name=u'email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=u'Designates whether the user can log into this admin site.', verbose_name=u'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=u'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=u'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=u'date joined')),
                ('gym', models.ForeignKey(to_field=u'id', blank=True, to='gyms.Gym', null=True)),
                ('level', models.IntegerField(blank=True, null=True, choices=[(10000, 'Owner'), (5000, 'Manager'), (1000, 'Setter'), (500, 'Employee')])),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name=u'groups', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name=u'user permissions', blank=True)),
            ],
            options={
                u'unique_together': set([('username', 'gym')]),
            },
            bases=(models.Model,),
        ),
    ]
