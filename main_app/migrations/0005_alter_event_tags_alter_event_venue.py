# Generated by Django 4.0.2 on 2022-04-04 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_merge_0002_event_user_0003_venue_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(to='main_app.Tag'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ManyToManyField(to='main_app.Venue'),
        ),
    ]