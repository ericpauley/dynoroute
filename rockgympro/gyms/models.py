from django.db import models
from django.conf import settings
import random
from django.utils import timezone
from django.db.models import Count
from collections import OrderedDict
from decimal import Decimal
from django.contrib.auth import get_user_model

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

class GymManager(models.Manager):

    def get_query_set(self):
        return super(GymManager, self).get_query_set()

class Gym(DatedMixin):

    objects = GymManager()

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=32)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name="gyms")

    location_options = models.TextField(blank=True)
    named_routes = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def num_live_routes(self):
        try:
            self._num_live_routes
        except AttributeError:
            self._num_live_routes = self.live_routes.count()
        return self._num_live_routes

    @property
    def live_routes(self):
        try:
            self._live_routes
        except AttributeError:
            print "blegh"
            self._live_routes = self.routes.filter(status="complete").exclude(date_torn__lte=timezone.now())
        return self._live_routes

    def types(self):
        d = OrderedDict([(Route(type=x['type']).get_type_display(),x['count']*1.0) for x in self.live_routes.values('type').annotate(count=Count("slug"))])
        return d if len(d) > 1 else {}

    def bouldering_grades(self):
        return self.grades(type="bouldering")

    def top_rope_grades(self):
        return self.grades(type="top_rope")

    def grades(self, **kwargs):
        d = OrderedDict([(x['grade'],x['count']*1.0) for x in self.live_routes.filter(**kwargs).values('grade').annotate(count=Count("slug"))])
        return d if len(d) > 1 else {}

    def setters(self):
        d = {get_user_model().objects.get(id=x['setter']).get_full_name() or get_user_model().objects.get(id=x['setter']).username if x['setter'] else 'Unknown':x['count']*1.0 for x in self.live_routes.values('setter').annotate(count=Count('slug'))}
        return d if len(d) > 1 else {}

    def locations(self):
        d = {x['location']:x['count']*1.0 for x in self.live_routes.values('location').annotate(count=Count('slug'))}
        return d if len(d) > 1 else {}

class Membership(DatedMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    gym = models.ForeignKey(Gym)

class Route(DatedMixin, SluggedMixin):
    name = models.CharField(blank=True, max_length=255)

    TYPE_CHOICES = (
        ('top_rope', 'Top Rope'),
        ('bouldering', 'Bouldering')
    )

    GRADE_CHOICES = (
        ('Top Rope', []),
        ('Bouldering', []),
    )

    for i in range(5,16):
        if i > 9:
            GRADE_CHOICES[0][1].append((Decimal(i-.25), "5.%s-" % i))
        GRADE_CHOICES[0][1].append((Decimal(i), "5.%s" % i))
        if i >= 9:
            GRADE_CHOICES[0][1].append((Decimal(i+.25), "5.%s+" % i))

    for i in range(0,14):
        GRADE_CHOICES[1][1].append((Decimal(1000+i-.25), "V%s-" % i))
        GRADE_CHOICES[1][1].append((Decimal(1000+i), "V%s" % i))
        GRADE_CHOICES[1][1].append((Decimal(1000+i+.25), "V%s+" % i))

    type = models.CharField(choices=TYPE_CHOICES, max_length=16, blank=False, default="bouldering")
    grade = models.DecimalField(choices=GRADE_CHOICES, blank=False, max_digits=10, decimal_places=2)
    setter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='routes', blank=True, null=True)
    location = models.CharField(max_length=32)
    date_set = models.DateField(default=timezone.now())
    date_torn = models.DateField(blank=True, null=True)
    gym = models.ForeignKey(Gym, related_name='routes')
    notes = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="route_images")
    sends = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Send", related_name="sends")
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Favorite", related_name="favorites")


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

class Send(DatedMixin, models.Model):
    route = models.ForeignKey(Route)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = (("route", "user"),)

class Favorite(DatedMixin, models.Model):
    route = models.ForeignKey(Route)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = (("route", "user"),)
