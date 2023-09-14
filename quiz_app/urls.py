from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('video_feed/', views.video_feed_view, name="video_feed"),
    path('quiz_movie/', views.quiz_movie_view, name="quiz_movie"),
    path('webcamera/', views.WebCameraView.as_view(), name="webcamera"),
]
urlpatterns += staticfiles_urlpatterns()