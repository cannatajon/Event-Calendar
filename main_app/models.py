from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Venue(models.Model):
    eventbrite_id = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
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
    created_user = models.IntegerField(default=0)
    user = models.ManyToManyField(User)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.CharField(default='https://soccerpointeclaire.com/wp-content/uploads/2021/06/default-profile-pic-e1513291410505.jpg', blank=True, null=True, max_length=3000)
    bio = models.TextField(default='edit my bio', max_length=250)
    def __str__(self):
        return self.user.username