# Generated by Django 4.1.6 on 2023-02-02 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='attendees',
            new_name='attendee',
        ),
    ]
