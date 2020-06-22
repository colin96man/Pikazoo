from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.contrib.localflavor.us.us_states import STATE_CHOICES

import petpy
import os
from petpy import Petfinder

key = os.environ['API_KEY']
secret = os.environ['API_SECRET']
pf = Petfinder(key, secret)

# Create your models here.

ACTIVITIES = (
    ('W', 'Walk'),
    ('P', 'Play'),
    ('G', 'Groom'),
    ('T', 'Train'),
)

ANIMAL_TYPES = (
    ('dog', 'Dogs'),
    ('cat', 'Cats'),
    ('rabbit', 'Rabbits'),
    ('small-furry', 'Small, furry animals'),
    ('horse', 'Horses'),
    ('bird', 'Birds'),
    ('scales-fins-other', 'Fish and reptiles'),
    ('barnyard', 'Barnyard animals'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(
        max_length=2,
        choices=STATE_CHOICES
    )
    pet_preference = models.CharField(
        max_length=100,
        choices=ANIMAL_TYPES,
        default=ANIMAL_TYPES[0][0]
    )




class Playdate(models.Model):
    animal_id = models.IntegerField()
    shelter_id = models.CharField(max_length=100)
    date = models.DateField('playdate date')
    activity = models.CharField(
        max_length=100,
        choices=ACTIVITIES,
        default=ACTIVITIES[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
