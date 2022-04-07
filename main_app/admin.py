from django.contrib import admin
from main_app.models import Event, Venue, Tag, Profile


# Register your models here.

admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Tag)

admin.site.register(Profile)
