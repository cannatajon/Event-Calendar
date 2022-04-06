# Generated by Django 4.0.2 on 2022-04-06 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_event_title'),
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
