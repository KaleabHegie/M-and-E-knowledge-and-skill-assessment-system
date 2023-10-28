# Generated by Django 4.2 on 2023-10-26 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey_managment', '0019_merge_20231026_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='choice_group',
        ),
        migrations.AlterField(
            model_name='question',
            name='catagory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.category'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='choice',
        ),
        migrations.AlterField(
            model_name='question',
            name='doc_label',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='label',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('Text', 'Text'), ('Number', 'Number'), ('Radio', 'Radio'), ('Checkbox', 'Checkbox'), ('Text-Area', 'Text Area'), ('URL', 'URL'), ('Email', 'Email'), ('Date', 'Date'), ('Rating', 'Rating')], max_length=100),
        ),
        migrations.AddField(
            model_name='question',
            name='choice',
            field=models.ManyToManyField(blank=True, null=True, to='survey_managment.choice'),
        ),
    ]
