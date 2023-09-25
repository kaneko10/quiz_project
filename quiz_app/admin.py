from django.contrib import admin

from .models import Question, PlayTime, QuizAnswerTime, Questionnaire, QuizOrder, Person


admin.site.register(Question)
admin.site.register(PlayTime)
admin.site.register(QuizAnswerTime)
admin.site.register(Questionnaire)
admin.site.register(QuizOrder)
admin.site.register(Person)