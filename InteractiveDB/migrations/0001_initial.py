# Generated by Django 4.1 on 2023-01-31 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recode', models.IntegerField()),
                ('choiceTextEnglish', models.TextField(blank=True, null=True)),
                ('choiceTextFrench', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionType', models.CharField(max_length=30)),
                ('questionName', models.CharField(max_length=30)),
                ('questionTextEnglish', models.TextField()),
                ('questionTextFrench', models.TextField()),
                ('questionThemeEnglish', models.TextField()),
                ('questionThemeFrench', models.TextField()),
                ('parentQuestionID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InteractiveDB.questiontable')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualtricsSurveyID', models.CharField(max_length=30)),
                ('releaseDate', models.DateField()),
                ('accessedDate', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('externalDataReference', models.CharField(max_length=15)),
                ('province', models.CharField(max_length=2)),
                ('size', models.CharField(max_length=6)),
                ('domain', models.CharField(max_length=30)),
                ('languagePreference', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponseTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerText', models.TextField(null=True)),
                ('answerValue', models.TextField(null=True)),
                ('choiceID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InteractiveDB.choicetable')),
                ('questionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InteractiveDB.questiontable')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='InteractiveDB.usertable')),
            ],
        ),
        migrations.AddField(
            model_name='questiontable',
            name='surveyID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InteractiveDB.surveytable'),
        ),
        migrations.AddField(
            model_name='choicetable',
            name='questionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InteractiveDB.questiontable'),
        ),
    ]
