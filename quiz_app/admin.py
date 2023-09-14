from django.contrib import admin

from .models import Question, PlayTime, QuizAnswerTime


admin.site.register(Question)
admin.site.register(PlayTime)
admin.site.register(QuizAnswerTime)