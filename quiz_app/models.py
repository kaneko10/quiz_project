from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class PlayTime(models.Model):
    play_time = models.CharField(max_length=30)

class QuizAnswerTime(models.Model):
    answer = models.CharField(max_length=50)
    time = models.CharField(max_length=30)

# アンケート
class Questionnaire(models.Model):
    q1 = models.CharField(max_length=30)
    q2_que = models.CharField(max_length=30)
    q2_ans = models.CharField(max_length=30)
    q3 = models.CharField(max_length=30)
    q4 = models.CharField(max_length=30)
    time = models.CharField(max_length=30)

class QuizOrder(models.Model):
    random_index = models.CharField(max_length=20)
    id_1 = models.CharField(max_length=20)
    id_2 = models.CharField(max_length=20)
    id_3 = models.CharField(max_length=20)
    id_4 = models.CharField(max_length=20)
    id_5 = models.CharField(max_length=20)
    id_6 = models.CharField(max_length=20)
    # id_7 = models.CharField(max_length=20)
    # id_8 = models.CharField(max_length=20)
    # id_9 = models.CharField(max_length=20)
    # id_10 = models.CharField(max_length=20)
    # id_11 = models.CharField(max_length=20)
    # id_12 = models.CharField(max_length=20)
    # id_13 = models.CharField(max_length=20)
    # id_14 = models.CharField(max_length=20)
    # id_15 = models.CharField(max_length=20)