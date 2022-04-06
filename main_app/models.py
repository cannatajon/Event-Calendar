from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Venue(models.Model):
    eventbrite_id = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    eventbrite_id = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.URLField(max_length=500, blank=True)
    tags = models.ManyToManyField(Tag)
    venue = models.ManyToManyField(Venue)
    location = models.CharField(max_length=50, blank=True)

    attendees = models.ManyToManyField(
        User, blank=True, related_name="attendees")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1)  # user id 1 is eventbrite

    def __str__(self):
        return str(self.id) + ' - ' + self.title


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.CharField(
        default='https://soccerpointeclaire.com/wp-content/uploads/2021/06/default-profile-pic-e1513291410505.jpg', blank=True, null=True, max_length=3000)
    bio = models.TextField(default='edit my bio', max_length=250)

    def __str__(self):
        return self.user.username
