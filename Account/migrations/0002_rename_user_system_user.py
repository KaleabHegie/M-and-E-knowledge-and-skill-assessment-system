# Generated by Django 4.2.5 on 2023-09-25 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='System_User',
        ),
    ]
