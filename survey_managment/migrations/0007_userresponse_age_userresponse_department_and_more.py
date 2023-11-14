# Generated by Django 4.2.7 on 2023-11-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_managment', '0006_userresponse_anonymous_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='age',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='year_of_experiance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
