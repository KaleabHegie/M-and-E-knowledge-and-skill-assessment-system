# Generated by Django 4.2.3 on 2023-11-07 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_line_ministry_alter_customuser_line_ministry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='Line_ministry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Account.line_ministry'),
        ),
    ]