# Generated by Django 4.2.7 on 2024-01-17 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_managment', '0005_category_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='question',
            field=models.ManyToManyField(blank=True, null=True, to='survey_managment.question'),
        ),
    ]
