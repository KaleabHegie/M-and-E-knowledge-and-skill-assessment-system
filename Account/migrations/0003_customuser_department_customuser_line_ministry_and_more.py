# Generated by Django 4.2.5 on 2023-10-05 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_customuser_date_of_birth_customuser_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Department',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='Line_ministry',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='Role',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
