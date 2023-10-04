from django.contrib import admin

from .models import PlayTime, QuizAnswerTime, Questionnaire, QuizOrder, Person, EndedTime, WhetherAnswer, PausedTime

admin.site.register(PlayTime)
admin.site.register(PausedTime)
admin.site.register(EndedTime)
admin.site.register(QuizAnswerTime)
admin.site.register(Questionnaire)
admin.site.register(QuizOrder)
admin.site.register(Person)
admin.site.register(WhetherAnswer)