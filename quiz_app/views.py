from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.template import loader

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from urllib.parse import urlencode

from .models import Question, PlayTime, QuizAnswerTime, Questionnaire, QuizOrder, Person
from .forms import PersonForm

import cv2
import datetime
import pytz
import json

person_id = ""

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("quiz/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

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
            return redirect('quiz_movie', person_id=name)
    else:
        form = PersonForm()

    return render(request, 'quiz/save_name.html', {'form': form})

# ストリーミング画像・映像を表示するview
class WebCameraView(View):
    def get(self, request):
        return render(request, 'quiz/webcamera.html', {})

# ストリーミング画像を定期的に返却するview
def video_feed_view(request):
    return StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

# フレーム生成・返却する処理
def generate_frame():
    global capture, video  # capture と video をグローバル変数として使用

    capture = cv2.VideoCapture(0)  # USBカメラから

    fps = int(capture.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
    video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

    while True:
        ret, frame = capture.read()
        
        if not ret:
            print("Failed to read frame.")
            break
        
        # 現在の時刻を取得
        jst = pytz.timezone('Asia/Tokyo')
        jst_now = datetime.datetime.now(jst)
        timestamp = jst_now.strftime("%Y-%m-%d %H:%M:%S")
        
        # タイムスタンプをフレーム上にオーバーレイ
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        video.write(frame)
        
        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()
        
        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
        
        # フレーム生成速度を調整するための一時停止
        # time.sleep(0.1)  # 0.1秒待機
    capture.release()
    video.release()

def stop_recording(request):
    global capture, video  # capture と video をグローバル変数として使用

    if capture and video:
        # カメラのキャプチャと動画保存を停止
        capture.release()
        video.release()
        capture = None
        video = None

        # video.mp4 ファイルをダウンロードさせる
        with open('video.mp4', 'rb') as file:
            print("ファイルをダウンロード")
            response = HttpResponse(file.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="video.mp4"'
    
        return response
    else:
        # キャプチャと動画が正しく初期化されていない場合の処理
        return HttpResponse("Recording not started.", status=400)

def quiz_movie_view(request, person_id):
    if request.method == "POST":
        print("POSTリクエスト")
        data = json.loads(request.body.decode('utf-8'))  # JSONデータを解析
        action = data.get('action')
        person_id = data.get('person_id')

        if action == 'play':
            # POSTリクエストからボタンが押された時刻を取得
            # 日本時間のタイムゾーンを取得
            jst = pytz.timezone('Asia/Tokyo')
            jst_now = datetime.datetime.now(jst)
            timestamp = jst_now.strftime("%Y-%m-%d %H:%M:%S")
            # ボタンが押された時刻をデータベースに保存
            PlayTime.objects.create(person_id=person_id, play_time=timestamp)
            print("save play movie time")

            quizIndex = data.get('quizIndex')
            quizIndex += 1
            print(f"Next Quiz Number {quizIndex}")
            
            # JSONレスポンスを返す（Ajaxリクエストに対応）
            return JsonResponse({"message": "Success", "quizIndex": quizIndex})
        elif action == 'answer':
            answer = data.get('answer')
            jst = pytz.timezone('Asia/Tokyo')
            jst_now = datetime.datetime.now(jst)
            timestamp = jst_now.strftime("%Y-%m-%d %H:%M:%S")
            QuizAnswerTime.objects.create(person_id=person_id, answer=answer, time=timestamp)
            print("save quiz answer and time")

            # JSONレスポンスを返す（Ajaxリクエストに対応）
            return JsonResponse({"message": "Success"})
        elif action == 'questionnaire':
            q1 = data.get('q1')
            q2_que = data.get('q2_que')
            q2_ans = data.get('q2_ans')
            q3 = data.get('q3')
            q4 = data.get('q4')
            # 日本時間のタイムゾーンを取得
            jst = pytz.timezone('Asia/Tokyo')
            jst_now = datetime.datetime.now(jst)
            timestamp = jst_now.strftime("%Y-%m-%d %H:%M:%S")
            # ボタンが押された時刻をデータベースに保存
            Questionnaire.objects.create(
                person_id=person_id,
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
            randoms = data.get('randoms')
            movie_ids = data.get('movie_ids')
            random_index = ""

            for index in randoms:
                print("index: " + str(index))
                random_index += str(index) + ", "

            QuizOrder.objects.create(
                person_id=person_id,
                random_index = random_index,
                id_1 = movie_ids[0],
                id_2 = movie_ids[1],
                id_3 = movie_ids[2],
                id_4 = movie_ids[3],
                id_5 = movie_ids[4],
                id_6 = movie_ids[5],
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
    return HttpResponse("You're looking at question %s." % person_id)