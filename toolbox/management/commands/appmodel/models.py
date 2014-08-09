from datetime import datetime, date, timedelta
from itertools import groupby
import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Count, Avg, Min, Max, Sum, Variance, StdDev
from django.db.models.signals import post_save

from tastypie.models import create_api_key

# from django.contrib.sites.models import Site
# Site.objects.get_or_create(domain='localhost', name='localhost')


def choices(labels):
    labels = labels.strip().split('\n')
    ids = range(1, len(labels)+1)
    ids = map(str, ids)
    return zip(ids, labels)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
post_save.connect(create_api_key, sender=User)


class Account(models.Model):
    user = models.OneToOneField(User)

# widgets = '''
# Table
# Line
# CurveLine
# Pie
# Donut
# Area
# StackedArea
# Bar
# StackedBar
# Column
# StackedColumn
# Histogram
# Number
# Word
# Scatter
# Bubble
# Calendar
# Geo
# Gauge
# '''
# SAMPLE_CHOICES = choices(widgets)
# class Sample(models.Model):
#     user = models.ForeignKey(User)
#     title = models.CharField(max_length=150)
#     columns = models.IntegerField(default=3)
#     public = models.BooleanField(default=False)
#     method = models.CharField(max_length=5, choices=SAMPLE_CHOICES, default='1')
#     real = models.DecimalField(decimal_places=2, max_digits=15)
#     real2 = models.FloatField()
#     data = models.TextField(max_length=5000)
#     timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)

#     def __str__(self):
#         return self.title


# from django_dynamic_fixture import G, F
# user = User.objects.all()[0]
# d = G(Sample, user=)
