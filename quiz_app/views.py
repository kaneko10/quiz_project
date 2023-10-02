from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.template import loader

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from urllib.parse import urlencode

from .models import PlayTime, QuizAnswerTime, Questionnaire, QuizOrder, Person, EndedTime
from .forms import PersonForm

import cv2
import datetime
import pytz
import json
import numpy as np
import base64
from io import BytesIO

person_id = ""

# 一番最初にアクセスして被験者の識別子を入力するview
def save_name(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # フォームのデータをデータベースに保存
            name = form.cleaned_data['name']
            print("person_id(save_name): " + name)

            redirect_url = redirect("quiz_movie", person_id=name)
            parameters = urlencode({"person_id": name})
            url = f"{redirect_url['Location']}?{parameters}"
            return redirect(url)

            # return render(request, 'quiz/quiz_movie.html', {"person_name": name})  # 保存が成功した場合、リダイレクト
            # return redirect('quiz_movie', person_id=name)
    else:
        form = PersonForm()

    return render(request, 'quiz/save_name.html', {'form': form})
    
def quiz_movie_view(request, person_id):
    if request.method == "POST":
        print("POSTリクエスト")
        data = json.loads(request.body.decode('utf-8'))  # JSONデータを解析
        action = data.get('action')
        person_id = data.get('person_id')
        timestamp = data.get('timestamp')

        if action == 'play':
            movie_id = data.get('movie_id')
            # ボタンが押された時刻をデータベースに保存
            PlayTime.objects.create(
                person_id=person_id, 
                movie_id=movie_id,
                play_time=timestamp,
            )
            print("save play movie time")
            
            # JSONレスポンスを返す（Ajaxリクエストに対応）
            return JsonResponse({"message": "Success"})
        elif action == 'answer':
            answer = data.get('answer')
            movie_id = data.get('movie_id')
            QuizAnswerTime.objects.create(
                person_id=person_id, 
                movie_id=movie_id,
                answer=answer, 
                time=timestamp
            )
            print("save quiz answer and time")

            # JSONレスポンスを返す（Ajaxリクエストに対応）
            return JsonResponse({"message": "Success"})
        elif action == 'ended':
            movie_id = data.get('movie_id')
            timestamp = data.get('timestamp')
            # ボタンが押された時刻をデータベースに保存
            EndedTime.objects.create(
                person_id=person_id, 
                movie_id=movie_id,
                ended_time=timestamp,
            )

            quizIndex = data.get('quizIndex')
            quizIndex += 1
            print(f"Next Quiz Number {quizIndex}")
            
            return JsonResponse({"message": "Success", "quizIndex": quizIndex})
        elif action == 'questionnaire':
            movie_id = data.get('movie_id')
            q1 = data.get('q1')
            q2_que = data.get('q2_que')
            q2_ans = data.get('q2_ans')
            q3 = data.get('q3')
            q4 = data.get('q4')
            # ボタンが押された時刻をデータベースに保存
            Questionnaire.objects.create(
                person_id=person_id,
                movie_id=movie_id,
                q1 = q1,
                q2_que = q2_que,
                q2_ans = q2_ans,
                q3 = q3,
                q4 = q4,
                time = timestamp
            )
            print("アンケート回答をデータベースに保存しました")
            return JsonResponse({"message": "Success"})
        
        elif action == 'quiz_order':
            randoms_mystery = data.get('randoms_mystery')
            randoms_riddle = data.get('randoms_riddle')
            movie_ids = data.get('movie_ids')
            random_index_mystery  = ""
            random_index_riddle  = ""

            for index in randoms_mystery:
                print("index: " + str(index))
                random_index_mystery += str(index) + ", "

            for index in randoms_riddle:
                print("index: " + str(index))
                random_index_riddle += str(index) + ", "

            QuizOrder.objects.create(
                person_id=person_id,
                time = timestamp,
                random_index_mystery = random_index_mystery,
                random_index_riddle = random_index_riddle,
                id_1 = movie_ids[0],
                id_2 = movie_ids[1],
                id_3 = movie_ids[2],
                id_4 = movie_ids[3],
                id_5 = movie_ids[4],
                id_6 = movie_ids[5],
                id_7 = movie_ids[6],
                id_8 = movie_ids[7],
                id_9 = movie_ids[8],
                id_10 = movie_ids[9],
                id_11 = movie_ids[10],
                id_12 = movie_ids[11],
                id_13 = movie_ids[12],
                id_14 = movie_ids[13],
                id_15 = movie_ids[14],
            )
            return JsonResponse({"message": "Success"})

    print("first access quiz_movie.html")
    person_id = request.GET.get('person_id', '')
    print("person_id: " + person_id)
    template = loader.get_template("quiz/quiz_movie.html")
    context = {
        "text": person_id,
        "isPlaying": False,
        "person_id": person_id,
    }
    param1 = request.GET.get("person_id")
    # return HttpResponse(f"POST: {person_id} <br>GET: {param1}")
    return HttpResponse(template.render(context, request))

# 実験1：表情を作成してもらう実験
def make_expression_view(request, person_id):
    if request.method == "POST":
        print("POSTリクエスト")
        data = json.loads(request.body.decode('utf-8'))  # JSONデータを解析
        action = data.get('action')
        person_id = data.get('person_id')

        if action == 'play':
            movie_id = data.get('movie_id')
            # POSTリクエストからボタンが押された時刻を取得
            # 日本時間のタイムゾーンを取得
            jst = pytz.timezone('Asia/Tokyo')
            jst_now = datetime.datetime.now(jst)
            timestamp = jst_now.strftime("%Y-%m-%d %H:%M:%S.%f")  # %f はマイクロ秒まで表示
            # ボタンが押された時刻をデータベースに保存
            PlayTime.objects.create(
                person_id=person_id,
                movie_id=movie_id,
                play_time=timestamp
            )
            print("save play movie time")

            quizIndex = data.get('quizIndex')
            quizIndex += 1
            print(f"Next Quiz Number {quizIndex}")
            
            # JSONレスポンスを返す（Ajaxリクエストに対応）
            return JsonResponse({"message": "Success", "quizIndex": quizIndex})

    print("first access make_expression.html")
    person_id = request.GET.get('person_id', '')
    print("person_id: " + person_id)
    template = loader.get_template("quiz/make_expression.html")
    context = {
        "person_id": person_id,
    }
    return HttpResponse(template.render(context, request))

# 実験1：一番最初にアクセスして被験者の識別子を入力するview
def save_name_expt1(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # フォームのデータをデータベースに保存
            name = form.cleaned_data['name']
            print("person_id(save_name): " + name)

            redirect_url = redirect("make_expression", person_id=name)
            parameters = urlencode({"person_id": name})
            url = f"{redirect_url['Location']}?{parameters}"
            return redirect(url)
    else:
        form = PersonForm()

    return render(request, 'quiz/save_name_expt1.html', {'form': form})