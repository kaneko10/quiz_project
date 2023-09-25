from django.contrib import admin

from .models import Question, PlayTime, QuizAnswerTime, Questionnaire


admin.site.register(Question)
admin.site.register(PlayTime)
admin.site.register(QuizAnswerTime)
admin.site.register(Questionnaire)