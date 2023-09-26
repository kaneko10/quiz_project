from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('video_feed/', views.video_feed_view, name="video_feed"),
    path('quiz_movie/<str:person_id>/', views.quiz_movie_view, name="quiz_movie"),
    path('webcamera/', views.WebCameraView.as_view(), name="webcamera"),
    path('stop_recording/', views.stop_recording, name='stop_recording'),   # 録画停止用の URL パターン
    path('save_name/', views.save_name, name='save_name'),
    path('make_expression/<str:person_id>/', views.make_expression_view, name='make_expression'),
    path('save_name_expt1/', views.save_name_expt1, name='save_name_expt1'),
]
urlpatterns += staticfiles_urlpatterns()