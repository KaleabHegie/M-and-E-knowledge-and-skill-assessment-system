# Generated by Django 5.0.1 on 2024-01-22 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_managment', '0005_category_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('Text', 'text'), ('number', 'number'), ('checkbox', 'checkbox'), ('radio', 'radio'), ('textarea', 'textarea'), ('url', 'url'), ('email', 'email'), ('date', 'date'), ('rating', 'rating')], max_length=100),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question',
            field=models.ManyToManyField(blank=True, null=True, to='survey_managment.question'),
        ),
    ]
