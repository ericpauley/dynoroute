from django.db import models
from django.conf import settings
import random
from django.utils import timezone

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
        ('Top Rope', []),
        ('Bouldering', []),
    )

    for i in range(5,16):
        if i > 9:
            RATING_CHOICES[0][1].append((i-.25, "5.%s-" % i))
        RATING_CHOICES[0][1].append((i, "5.%s" % i))
        if i >= 9:
            RATING_CHOICES[0][1].append((i+.25, "5.%s+" % i))

    for i in range(0,14):
        RATING_CHOICES[1][1].append((i-.25, "V%s-" % i))
        RATING_CHOICES[1][1].append((i, "V%s" % i))
        RATING_CHOICES[1][1].append((i+.25, "V%s+" % i))

    type = models.CharField(choices=TYPE_CHOICES, max_length=16, blank=False, default="bouldering")
    difficulty = models.FloatField(choices=RATING_CHOICES, blank=False)
    setter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='routes')
    location = models.CharField(max_length=32)
    date_set = models.DateField(default=timezone.now())
    date_torn = models.DateField(blank=True, null=True)
    gym = models.ForeignKey(Gym, related_name='routes')
    notes = models.TextField(blank=True)

    STATUS_CHOICES = (
        ('complete', 'Complete'),
        ('in_progress', 'In Progress'),
        ('not_started', 'Not Started'),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=16, blank=False, default="complete")

    COLOR_CHOICES=(
        ("#ffffff","Clear"),
        ("#d11f2d","Red"),
        ("#fef102","Yellow"),
        ("#FF6500","Orange"),
        ("#ed7696","Pink"),
        ("#6f3728","Dark Brown"),
        ("#bd955a","Light Brown"),
        ("#00b2e2","Light Blue"),
        ("#094080","Dark Blue"),
        ("#01b703","Lime Green"),
        ("#f2f2f2","White"),
        ("#009ca8","Teal"),
        ("#007a41","Dark Green"),
        ("#000000","Black"),
        ("#724c9f","Purple"),
    )

    color1 = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#ffffff")
    color2 = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#ffffff")
    
    @property 
    def formatted_difficulty(self):
        routeType = dict(Route.TYPE_CHOICES)[self.type]
        return dict(dict(Route.RATING_CHOICES)[routeType])[self.difficulty]
