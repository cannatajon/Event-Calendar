# Generated by Django 4.0.3 on 2022-04-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_tag_venue_event_eventbrite_id_event_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]