from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.template import loader

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import Question, PlayTime

import cv2
import datetime
import pytz


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

# ストリーミング画像・映像を表示するview
class WebCameraView(View):
    def get(self, request):
        return render(request, 'quiz/webcamera.html', {})

# ストリーミング画像を定期的に返却するview
def video_feed_view(request):
    return StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

# フレーム生成・返却する処理
def generate_frame():
    capture = cv2.VideoCapture(0)  # USBカメラから

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
        
        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()
        
        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
        
        # フレーム生成速度を調整するための一時停止
        # time.sleep(0.1)  # 0.1秒待機
    capture.release()



# # ストリーミング画像を定期的に返却するview
# def video_feed_view():
#     return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

# # フレーム生成・返却する処理
# def generate_frame():
#     capture = cv2.VideoCapture(0)  # USBカメラから

#     fps = int(capture.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
#     w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
#     h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
#     fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
#     video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

#     while True:
#         if not capture.isOpened():
#             print("Capture is not opened.")
#             break
#         # カメラからフレーム画像を取得
#         ret, frame = capture.read()
#          # 現在の時刻を取得
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         # タイムスタンプをフレーム上にオーバーレイ
#         cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         video.write(frame)                                     # 動画を1フレームずつ保存する
#         if not ret:
#             print("Failed to read frame.")
#             break
#         # フレーム画像バイナリに変換
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         byte_frame = jpeg.tobytes()
#         # フレーム画像のバイナリデータをユーザーに送付する
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
#     capture.release()

# def quiz_movie_view(request):
#     if request.method == "POST":
#         print("PlayTime")
#         # ボタンが押された時刻をデータベースに保存
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         PlayTime.objects.create(play_time=timestamp)
#         context = {
#             "text": "text",
#             "isPlaying": True
#         }
#         return render(request, "quiz/quiz_movie.html", context)
    
#     print("aaaaa")
#     template = loader.get_template("quiz/quiz_movie.html")
#     context = {
#         "text": "text",
#         "isPlaying": False
#     }
#     return HttpResponse(template.render(context, request))

def quiz_movie_view(request):
    if request.method == "POST":
        print("save play movie time")
        # POSTリクエストからボタンが押された時刻を取得
        # 日本時間のタイムゾーンを取得
        jst = pytz.timezone('Asia/Tokyo')
        jst_now = datetime.datetime.now(jst)
        timestamp = jst_now.strftime("%Y-%m-%d %H:%M:%S")
        
        # ボタンが押された時刻をデータベースに保存
        PlayTime.objects.create(play_time=timestamp)
        
        # JSONレスポンスを返す（Ajaxリクエストに対応）
        return JsonResponse({"message": "Success"})

    print("first access quiz_movie.html")
    template = loader.get_template("quiz/quiz_movie.html")
    context = {
        "text": "text",
        "isPlaying": False
    }
    return HttpResponse(template.render(context, request))