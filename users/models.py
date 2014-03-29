from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
import functools

perms = [
"admin_view",
"routes_view",
"routes_manage",
"staff_manage",
"team_admin_view",
"owner",
]

@functools.total_ordering
class EmployeeBase(object):

    def __getattr__(self, key):
        try:
            return getattr(super(EmployeeBase, self), key)
        except AttributeError:
            if key in perms:
                return None
            else:
                raise AttributeError

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __gt__(self, other):
        try:
            return self.level > other.level
        except AttributeError:
            return self > levels[other.lower()]

    def __eq__(self, other):
        try:
            return self.level == other.level
        except AttributeError:
            return self == levels[other.lower()]

class Employee(EmployeeBase):

    name = "Employee"
    level = 500
    admin_view = True
    routes_view = True

class Setter(Employee):

    name = "Setter"
    level = 1000

    routes_manage = True

class Manager(Setter):

    name = "Manager"
    level = 5000
    staff_manage = True

class HeadCoach(EmployeeBase):

    name = "Head Coach"
    level = 900
    team_admin_view = True

class Owner(Manager, HeadCoach):

    name = "Owner"
    level = 10000
    owner = True

levels = {
    "employee": Employee(),
    "setter": Setter(),
    "manager": Manager(),
    "headcoach": HeadCoach(),
    "owner": Owner(),
}

class UserManager(UserManager):

    def get_by_natural_key(self, username):
        parts = username.split(":")
        if len(parts) == 1:
            return self.get(**{"username": parts[0]})
        elif len(parts) == 2:
            return self.get(**{"gym__slug":parts[0], "username": parts[1]})
        else:
            raise self.model.DoesNotExist("No more than one ':' allowed in usernames.")

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])
    name = models.CharField(_('first name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    gym = models.ForeignKey('gyms.Gym', related_name="staff", blank=True, null=True)

    MEMBERSHIP_LEVELS = (
        (10000, levels["owner"]),
        (5000, levels["manager"]),
        (1000, levels["setter"]),
        (500, levels["employee"]),
        (900, levels["headcoach"]),
    )
    level = models.IntegerField(choices=MEMBERSHIP_LEVELS, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        unique_together = (("username", "gym"),)

    @property
    def perms(self):
        return dict(self.MEMBERSHIP_LEVELS)[self.level]

    def get_username(self):
        if self.gym is not None:
            return "%s:%s" % (self.gym.slug, self.username)
        else:
            return self.username

    def clean(self):
         if self.gym and not self.level:
            self.level = 500

    def initials(self):
        return "".join([part[:1] for part in self.name.split()])

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.name.strip() or self.username

    def get_short_name(self):
        "Returns the short name for the user."
        if self.name:
            return self.name.split()[0]
        else:
            return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        return self.get_full_name() or self.username
