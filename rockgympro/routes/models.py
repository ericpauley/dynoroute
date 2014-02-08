from django.db import models
from django.contrib.auth.models import User

class Gym(models.Model):
    name = models.CharField()

class Route(models.Model):
    name = models.CharField(blank=True)

    TYPE_CHOICES = (
        ('top_rope', 'Top Rope'),
        ('bouldering', 'Bouldering')
    )

    RATING_MAPS = {
        'top_rope': {
            0:  '5.0',
            1:  '5.1',
            2:  '5.2',
            3:  '5.3',
            4:  '5.4',
            5:  '5.5',
            6:  '5.6',
            7:  '5.7',
            8:  '5.8',
            9:  '5.9',
            10: '5.10',
            11: '5.11',
            12: '5.12',
            13: '5.13',
            14: '5.14',
            15: '5.15',
        },
        'bouldering': {
            0:  'V0',
            1:  'V1',
            2:  'V2',
            3:  'V3',
            4:  'V4',
            5:  'V5',
            6:  'V6',
            7:  'V7',
            8:  'V8',
            9:  'V9',
            10: 'V10',
            11: 'V11',
            12: 'V12',
            13: 'V13',
            14: 'V14',
            15: 'V15',
            16: 'V16',
        }
    }

    type = models.CharField(choices=TYPE_CHOICES)
    difficulty = models.IntegerField()
    setter = models.ForeignKey(User)
    date_set = models.DateField()
    gym = models.ForeignKey(Gym)

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
