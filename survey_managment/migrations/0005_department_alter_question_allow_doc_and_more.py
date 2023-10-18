# Generated by Django 4.2.5 on 2023-10-14 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey_managment', '0004_remove_answer_forquestion_remove_answer_response_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_no', models.IntegerField()),
                ('department_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='allow_doc',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='doc_label',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='has_weight',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='label',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='weight',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='instruction',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now=True)),
                ('submitted_id', models.CharField(max_length=100)),
                ('forsurvey', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.survey')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answertext', models.CharField(max_length=500)),
                ('forquestion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.question')),
                ('response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.userresponse')),
            ],
        ),
    ]