from django.db import models

class PlayTime(models.Model):
    person_id = models.CharField(max_length=30)
    movie_id = models.CharField(max_length=30)
    play_time = models.CharField(max_length=30)

class EndedTime(models.Model):
    person_id = models.CharField(max_length=30)
    movie_id = models.CharField(max_length=30)
    ended_time = models.CharField(max_length=30)

class QuizAnswerTime(models.Model):
    person_id = models.CharField(max_length=30)
    movie_id = models.CharField(max_length=30)
    answer = models.CharField(max_length=50)
    time = models.CharField(max_length=30)

# アンケート
class Questionnaire(models.Model):
    person_id = models.CharField(max_length=30)
    movie_id = models.CharField(max_length=30)
    q1 = models.CharField(max_length=30)
    q2_que = models.CharField(max_length=30)
    q2_ans = models.CharField(max_length=30)
    q3 = models.CharField(max_length=30)
    q4 = models.CharField(max_length=30)
    q5 = models.CharField(max_length=30)
    time = models.CharField(max_length=30)

class QuizOrder(models.Model):
    person_id = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    random_index_mystery = models.CharField(max_length=20)
    random_index_riddle = models.CharField(max_length=20)
    id_1 = models.CharField(max_length=20)
    id_2 = models.CharField(max_length=20)
    id_3 = models.CharField(max_length=20)
    id_4 = models.CharField(max_length=20)
    id_5 = models.CharField(max_length=20)
    id_6 = models.CharField(max_length=20)
    id_7 = models.CharField(max_length=20)
    id_8 = models.CharField(max_length=20)
    id_9 = models.CharField(max_length=20)
    id_10 = models.CharField(max_length=20)
    id_11 = models.CharField(max_length=20)
    id_12 = models.CharField(max_length=20)
    id_13 = models.CharField(max_length=20)
    id_14 = models.CharField(max_length=20)
    id_15 = models.CharField(max_length=20)

class Person(models.Model):
    id_str = models.CharField(verbose_name='ID', max_length=10)
    name = models.CharField(verbose_name='名前', max_length=30)

class WhetherAnswer(models.Model):
    id_str = models.CharField(verbose_name='ID', max_length=10)
    name = models.CharField(max_length=30)
    whether_answer = models.BooleanField()