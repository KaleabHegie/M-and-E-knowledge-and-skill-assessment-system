# Generated by Django 4.2.7 on 2023-11-26 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_managment', '0005_userresponse_recommendation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='recommendation',
        ),
        migrations.AddField(
            model_name='answer',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
