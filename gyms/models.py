from django.db import models
from django.conf import settings
import random
from django.utils import timezone
from django.db.models import Count
from collections import OrderedDict
from decimal import Decimal
from django.contrib.auth import get_user_model
import datetime
from hashlib import sha256
import base64

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

    def get_queryset(self):
        return super(GymManager, self).get_queryset()

def logo_upload(self, filename):
    return "gym_images/%s.%s" % (self.slug, filename.split(".")[-1])

def about_image_upload(self, filename):
    return "gym_about_images/%s.%s" % (self.slug, filename.split(".")[-1])

rating_scales = {}

def build_ratings():
    scale = []
    for i in range(5,16):
        
        if i > 9:
            scale.append((Decimal(i-.25), "5.%s-" % i))
        scale.append((Decimal(i), "5.%s" % i))
        if i >= 9:
            scale.append((Decimal(i+.25), "5.%s+" % i))
    rating_scales['yds_plusminus'] = scale

    scale = []
    for i in range(5,16):
        if i > 9:
            scale.append((Decimal(i), "5.%sa" % i))
            scale.append((Decimal(i+.25), "5.%sb" % i))
            scale.append((Decimal(i+.5), "5.%sc" % i))
            if i < 15:
                scale.append((Decimal(i-.75), "5.%sd" % i))
        else:
            scale.append((Decimal(i), "5.%s" % i))

    rating_scales['yds_abcd'] = scale

    scale = []
    for i in range(0,14):
        scale.append((Decimal(1000+i-.25), "V%s-" % i))
        scale.append((Decimal(1000+i), "V%s" % i))
        scale.append((Decimal(1000+i+.25), "V%s+" % i))

    rating_scales['hueco'] = scale

    rating_scales['riao'] = [
        (1001, "REC"),
        (1004, "INT"),
        (1007, "ADV"),
        (1010, "OPEN"),
    ]

    rating_scales['french'] = [
        (Decimal(4), "4a"),
        (Decimal(5), "4b"),
        (Decimal(6), "4c"),
        (Decimal(7), "5a"),
        (Decimal(8), "5b"),
        (Decimal(9), "5c"),
        (Decimal(10), "6a"),
        (Decimal(10.25), "6a+"),
        (Decimal(10.5), "6b"),
        (Decimal(10.75), "6b+"),
        (Decimal(11.25), "6c"),
        (Decimal(11.5), "6c+"),
        (Decimal(11.75), "7a"),
        (Decimal(12), "7a+"),
        (Decimal(12.25), "7b"),
        (Decimal(12.5), "5b+"),
        (Decimal(12.75), "7c"),
        (Decimal(13), "7c+"),
        (Decimal(13.25), "8a"),
        (Decimal(13.5), "8a+"),
        (Decimal(13.75), "8b"),
        (Decimal(14), "8b+"),
        (Decimal(14.25), "8c"),
        (Decimal(14.5), "8c+"),
        (Decimal(14.75), "9a"),
        (Decimal(15), "9a+"),
        (Decimal(15.25), "9b"),
        (Decimal(15.5), "9b+"),
    ]

    rating_scales['font'] = [
        (Decimal(999.75), "4-"),
        (Decimal(1000), "4"),
        (Decimal(1000.25), "4+"),
        (Decimal(1001), "5"),
        (Decimal(1002), "5+"),
        (Decimal(1003), "6A"),
        (Decimal(1003.5), "6A+"),
        (Decimal(1004), "6B"),
        (Decimal(1004.5), "6B+"),
        (Decimal(1005), "6C"),
        (Decimal(1005.5), "6C+"),
        (Decimal(1006), "7A"),
        (Decimal(1007), "7A+"),
        (Decimal(1008), "7B"),
        (Decimal(1008.5), "7B+"),
        (Decimal(1009), "7C"),
        (Decimal(1010), "7C+"),
        (Decimal(1011), "8A"),
        (Decimal(1012), "8A+"),
        (Decimal(1013), "8B"),
        (Decimal(1014), "8B+"),
        (Decimal(1015), "8C"),
        (Decimal(1016), "8C+"),
    ]

build_ratings()

class Gym(DatedMixin):

    objects = GymManager()

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=32)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GymFollow', related_name="gyms")

    location_options = models.TextField(blank=True)
    named_routes = models.BooleanField(default=False)

    logo = models.ImageField(blank=True, upload_to=logo_upload)

    website_url = models.URLField(blank=True)
    phone = models.CharField("Phone Number", blank=True, null=True, max_length=255)
    address = models.TextField(blank=True, null=True)
    desc = models.TextField("Description", blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=about_image_upload)

    TAPE_COLOR_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )

    tape_colors = models.IntegerField(default=2, choices=TAPE_COLOR_CHOICES)

    TOP_ROPE_FORMAT_CHOICES = (
        ("yds_abcd", "YDS ABCD"),
        ("yds_plusminus", "YDS +/-"),
        ("french", "French")
    )

    BOULDERING_FORMAT_CHOICES = (
        ("hueco", "Hueco"),
        ("riao", "RIAO"),
        ("font", "Font")
    )

    top_rope_format = models.CharField(max_length=16, choices=TOP_ROPE_FORMAT_CHOICES, default="yds_plusminus")
    lead_format = models.CharField(max_length=16, choices=TOP_ROPE_FORMAT_CHOICES, default="yds_plusminus")
    bouldering_format = models.CharField(max_length=16, choices=BOULDERING_FORMAT_CHOICES, default="hueco")

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

class GymFollow(DatedMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    gym = models.ForeignKey(Gym)

    class Meta:
        unique_together = (("gym", "user"),)

class RouteManager(models.Manager):
    def get_queryset(self):
        return super(RouteManager, self).get_queryset().annotate(score=models.Avg('rating__score'), num_flags=models.Count('routeflag'))

def get_image_name(self, filename):
        sha = sha256()
        f = self.image
        sha.update(f.read())
        f.seek(0)
        return "route_images/%s.%s" % (base64.urlsafe_b64encode(sha.digest()).replace("=","_"), filename.split(".")[-1])

class Route(DatedMixin, SluggedMixin):
    name = models.CharField(blank=True, max_length=255)

    objects = RouteManager()

    TYPE_CHOICES = (
        ('top_rope', 'Top Rope'),
        ('bouldering', 'Bouldering'),
        ('lead', 'Lead'),
    )

    type = models.CharField(choices=TYPE_CHOICES, max_length=16, blank=False, default="bouldering")
    grade = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    setter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='routes', blank=True, null=True)
    location = models.CharField(max_length=32)
    date_set = models.DateField(default=datetime.date.today)
    date_torn = models.DateField(blank=True, null=True)
    gym = models.ForeignKey(Gym, related_name='routes')
    notes = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=get_image_name)
    sends = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Send", related_name="sends")
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Favorite", related_name="favorites")
    views = models.IntegerField(default=0)

    STATUS_CHOICES = (
        ('complete', 'Complete'),
        ('in_progress', 'In Progress'),
        ('not_started', 'Not Started'),
        ('torn', 'Torn'),
    )

    def get_grade(self):
        if self.grade is None:
            return None
        format = getattr(self.gym, "%s_format" % self.type)
        grade_list = sorted(rating_scales[format], key=lambda x:abs(x[0]-self.grade))
        return grade_list[0][0]

    def get_grade_display(self):
        if self.grade is None:
            return None
        format = getattr(self.gym, "%s_format" % self.type)
        grade_list = sorted(rating_scales[format], key=lambda x:abs(x[0]-self.grade))
        return grade_list[0][1]

    def colors(self):
        return [color for color in [self.color1, self.color2, self.color3] if color !="#ffffff"]

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
    color3 = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#ffffff")

    def save(self, *args, **kwargs):
        if self.status == 'torn':
            if not self.date_torn:
                self.date_torn = datetime.date.today()
        else:
            self.date_torn = None
        super(Route, self).save(*args, **kwargs)

class RouteUserMixin(models.Model):
    route = models.ForeignKey(Route)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = (("route", "user"),)
        abstract = True

class RouteFlag(DatedMixin, models.Model):
    route = models.ForeignKey(Route)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    message = models.TextField()

class Send(DatedMixin, RouteUserMixin, models.Model):
    pass

class Favorite(DatedMixin, RouteUserMixin, models.Model):
    pass

class Rating(DatedMixin, RouteUserMixin, models.Model):
    score = models.IntegerField()
