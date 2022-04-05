from django.contrib import admin
from main_app.models import Event, Venue, Tag

# Register your models here.

admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Tag)
