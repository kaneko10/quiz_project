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