from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='survey_managment.catagory')),
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
            name='Choice_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('instruction', models.TextField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('label', models.CharField(max_length=100)),
                ('question_type', models.CharField(choices=[('Text', 'Text'), ('Number', 'Number'), ('Radio', 'Radio'), ('Select', 'Select'), ('Multi-Select', 'Multi-Select'), ('Text-Area', 'Text Area'), ('URL', 'URL'), ('Email', 'Email'), ('Date', 'Date'), ('Rating', 'Rating')], max_length=100)),
                ('has_weight', models.BooleanField()),
                ('weight', models.IntegerField()),
                ('allow_doc', models.BooleanField()),
                ('doc_label', models.TextField()),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_managment.catagory')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_managment.choice')),
                ('choice_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_managment.choice_group')),
                ('for_questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_managment.questionnaire')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='for_choice_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_managment.choice_group'),
        ),
    ]