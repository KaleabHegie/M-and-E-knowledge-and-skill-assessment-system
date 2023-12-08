# Generated by Django 4.2.7 on 2023-12-04 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_managment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=150)),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('draft', 'Draft'), ('inbox', 'Inbox'), ('trash', 'Trash')], max_length=10, null=True)),
                ('to', models.CharField(max_length=50)),
            ],
        ),
    ]
