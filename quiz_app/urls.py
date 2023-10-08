from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('expt1/', views.input_name_expt1, name='input_name_expt1'),    # 最初にアクセス
    path('make_expression/<str:person_id>/', views.make_expression_view, name='make_expression'),
    path('expt2/<str:person_id>/', views.input_name_expt2, name='input_name_expt2'),
    path('quiz_movie/<str:person_id>/', views.quiz_movie_view, name="quiz_movie"),
]
urlpatterns += staticfiles_urlpatterns()