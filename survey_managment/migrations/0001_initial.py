# Generated by Django 4.2.3 on 2023-11-02 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='survey_managment.category')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_no', models.IntegerField()),
                ('department_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('label', models.TextField(blank=True, null=True)),
                ('question_type', models.CharField(choices=[('Text', 'Text'), ('Number', 'Number'), ('Radio', 'Radio'), ('Checkbox', 'Checkbox'), ('Text-Area', 'Text Area'), ('URL', 'URL'), ('Email', 'Email'), ('Date', 'Date'), ('Rating', 'Rating')], max_length=100)),
                ('has_weight', models.BooleanField(blank=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('allow_doc', models.BooleanField(blank=True)),
                ('doc_label', models.TextField(blank=True, null=True)),
                ('catagory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.category')),
                ('choice', models.ManyToManyField(blank=True, null=True, to='survey_managment.choice')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('instruction', models.TextField(null=True)),
                ('start_at', models.DateField(null=True)),
                ('end_at', models.DateField(null=True)),
                ('created_at', models.DateField(auto_now=True)),
                ('question', models.ManyToManyField(null=True, to='survey_managment.question')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now=True)),
                ('submitted_id', models.CharField(blank=True, max_length=50, null=True)),
                ('forsurvey', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.survey')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='survey',
            name='survey_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='survey_managment.surveytype'),
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
