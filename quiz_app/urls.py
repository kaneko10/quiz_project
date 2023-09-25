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
    path('quiz_movie/<str:person_id>/', views.quiz_movie_view, name="quiz_movie"),
    path('webcamera/', views.WebCameraView.as_view(), name="webcamera"),
    # 録画停止用の URL パターン
    path('stop_recording/', views.stop_recording, name='stop_recording'),
    path('save_name/', views.save_name, name='save_name'),
    path('make_expression/<str:person_id>/', views.make_expression_view, name='make_expression'),
    path('save_name_expt1/', views.save_name_expt1, name='save_name_expt1'),
]
urlpatterns += staticfiles_urlpatterns()