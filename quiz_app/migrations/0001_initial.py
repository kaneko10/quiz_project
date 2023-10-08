# Generated by Django 4.1.2 on 2023-10-08 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EndedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=30)),
                ('movie_id', models.CharField(max_length=30)),
                ('ended_time', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=10, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PlayTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=30)),
                ('movie_id', models.CharField(max_length=30)),
                ('play_time_0s', models.CharField(default=None, max_length=30)),
                ('play_time_1s', models.CharField(default=None, max_length=30)),
                ('current_movie_time', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=30)),
                ('movie_id', models.CharField(max_length=30)),
                ('q1', models.CharField(max_length=30)),
                ('q2_que', models.CharField(max_length=30)),
                ('q2_ans', models.CharField(max_length=30)),
                ('q3', models.CharField(max_length=30)),
                ('q4', models.CharField(max_length=30)),
                ('q5', models.CharField(max_length=30)),
                ('time', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswerTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=30)),
                ('movie_id', models.CharField(max_length=30)),
                ('answer', models.CharField(max_length=50)),
                ('time', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='QuizOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=30)),
                ('time', models.CharField(max_length=30)),
                ('random_index_mystery', models.CharField(max_length=20)),
                ('random_index_riddle', models.CharField(max_length=20)),
                ('id_1', models.CharField(max_length=20)),
                ('id_2', models.CharField(max_length=20)),
                ('id_3', models.CharField(max_length=20)),
                ('id_4', models.CharField(max_length=20)),
                ('id_5', models.CharField(max_length=20)),
                ('id_6', models.CharField(max_length=20)),
                ('id_7', models.CharField(max_length=20)),
                ('id_8', models.CharField(max_length=20)),
                ('id_9', models.CharField(max_length=20)),
                ('id_10', models.CharField(max_length=20)),
                ('id_11', models.CharField(max_length=20)),
                ('id_12', models.CharField(max_length=20)),
                ('id_13', models.CharField(max_length=20)),
                ('id_14', models.CharField(max_length=20)),
                ('id_15', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StopRecordTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=30)),
                ('time', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WhetherAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=10, verbose_name='ID')),
                ('whether_answer', models.BooleanField()),
            ],
        ),
    ]
