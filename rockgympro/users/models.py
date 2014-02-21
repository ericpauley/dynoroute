from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    gym = models.ForeignKey('gyms.Gym', related_name="staff", blank=True, null=True)

    MEMBERSHIP_LEVELS = (
        (5000, 'Manager'),
        (1000, 'Setter'),
        (500, 'Employee'),
    )
    level = models.IntegerField(choices=MEMBERSHIP_LEVELS, blank=True, null=True)

    def clean(self):
         if self.gym and not self.level:
            self.level = 500
