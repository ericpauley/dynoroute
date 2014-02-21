from django.db import models
from django.conf import settings
import random

class DatedMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SluggedMixin(models.Model):
    slug = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        while not self.slug:
            newslug = "".join(random.sample('1234567890abcdefghjkmnpqrstuvwxyz', 5))
            if self.__class__.objects.filter(slug=newslug).count() == 0:
                self.slug = newslug
        super(SluggedMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Gym(DatedMixin):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=32)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name="gyms")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_gyms")

    def __unicode__(self):
        return self.name 

class Membership(DatedMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    gym = models.ForeignKey(Gym)

class Route(DatedMixin, SluggedMixin):
    name = models.CharField(blank=True, max_length=255)

    TYPE_CHOICES = (
        ('top_rope', 'Top Rope'),
        ('bouldering', 'Bouldering')
    )

    RATING_CHOICES = (
        ('Top Rope', (
            (0,  '5.0'),
            (1,  '5.1'),
            (2,  '5.2'),
            (3,  '5.3'),
            (4,  '5.4'),
            (5,  '5.5'),
            (6,  '5.6'),
            (7,  '5.7'),
            (8,  '5.8'),
            (9,  '5.9'),
            (10, '5.10'),
            (11, '5.11'),
            (12, '5.12'),
            (13, '5.13'),
            (14, '5.14'),
            (15, '5.15'),
            )
        ),
        ('Bouldering', (
            (1000,  'V0'),
            (1001,  'V1'),
            (1002,  'V2'),
            (1003,  'V3'),
            (1004,  'V4'),
            (1005,  'V5'),
            (1006,  'V6'),
            (1007,  'V7'),
            (1008,  'V8'),
            (1009,  'V9'),
            (1010, 'V10'),
            (1011, 'V11'),
            (1012, 'V12'),
            (1013, 'V13'),
            (1014, 'V14'),
            (1015, 'V15'),
            (1016, 'V16'),
            )
        ),
    )

    type = models.CharField(choices=TYPE_CHOICES, max_length=16, blank=False)
    difficulty = models.IntegerField(choices=RATING_CHOICES, blank=False)
    setter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='routes')
    date_set = models.DateField()
    date_torn = models.DateField(blank=True, null=True)
    gym = models.ForeignKey(Gym, related_name='routes')
    
    @property 
    def formatted_difficulty(self):
        routeType = dict(Route.TYPE_CHOICES)[self.type]
        return dict(Route.RATING_CHOICES)[routeType][self.difficulty][1]
