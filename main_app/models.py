from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Venue(models.Model):
    eventbrite_id = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    address = models.TextField()


class Event(models.Model):
    eventbrite_id = models.CharField(max_length=16, blank=True)
    title = models.TextField()
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.URLField(max_length=500, blank=True)
    tags = models.ManyToManyField(Tag)
    venue = models.ManyToManyField(Venue)
