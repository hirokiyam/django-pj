from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import AIAnalysisLog # 保存するモデルをインポート
import requests
import time
import json

def home_view(request):
    return HttpResponse('')

@csrf_exempt
@require_POST
def save_response(request):
    # リクエストボディをPythonの辞書に変換して request_body に代入。内部に image_path が含まれる
    request_body = json.loads(request.body)

    # 上記検証用のモック
    # request_body = {
    #     "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"
    # }

    image_path = request_body.get('image_path') # DBに保存する用
    # 以下のような値になることを想定
    # "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"

    if not image_path:
        return JsonResponse({'status': 'error', 'message': 'No image path provided.'}, status=400)

    # 叩くURIは [ドメイン/api/endpoint] と仮定
    url = "http://example.com/api/endpoint"

    # リクエストのタイムスタンプ
    request_timestamp = int(time.time())

    try:
        # 外部APIへPOSTリクエストを送信
        # reequest.body で渡されたパラメーター(image_pathを想定)をjsonで渡しAPIを叩く
        response = requests.post(url, json=request_body)

        # 成功検証用のレスポンスモック
        # response_data = {
        #     "success": True,
        #     "message": "success",
        #     "estimated_data": {
        #         "class": 3,
        #         "confidence": 0.8683
        #     }
        # }

        # 失敗検証用のレスポンスモック
        # response_data = {
        #     "success": False,
        #     "message": "Error:E50012",
        #     "estimated_data": {}
        # }

        # レスポンスのタイムスタンプ
        response_timestamp = int(time.time())

        # レスポンスの JSON を Pythonの辞書に変換
        response_data = response.json()

        # AIAnalysisLogの共通カラムを設定
        log_data = {
            "image_path": image_path,
            "success": response_data.get('success', None),
            "message": response_data.get('message', None),
            "request_timestamp": request_timestamp,
            "response_timestamp": response_timestamp,
        }

        # レスポンスが成功の場合、追加データをセット
        if response.status_code == 200:
        # if True: # 成功検証時はこちらを使用
        # if False: # 失敗検証時はこちらを使用
            # 辞書にキーと値を追加する
            log_data.update({
                "class_field": response_data.get('estimated_data', {}).get('class', None),
                "confidence": response_data.get('estimated_data', {}).get('confidence', None),
            })
            # 保存を行う。辞書のキーと値のペアをキーワード引数として関数に渡す。
            AIAnalysisLog.objects.create(**log_data)

            # JSONレスポンスを返す
            return JsonResponse({'status': 'success', 'message': 'API response saved successfully.'})
        else:
            # 追加データはないのでそのまま保存を行う
            AIAnalysisLog.objects.create(**log_data)
            # エラーレスポンスをクライアントに返す
            return JsonResponse({'status': 'error', 'message': 'External API error.'}, status=response.status_code)
            # モックデータ（失敗）検証時は以下を使用（ステータスコードを入れるため）
            # return JsonResponse({'status': 'error', 'message': 'External API error.'}, status=400)


    except requests.exceptions.RequestException as e:
        # リクエストに失敗した場合

        log_data = {
            "image_path": image_path,
            "success": False,
            "message": str(e),
            "request_timestamp": request_timestamp,
            "response_timestamp": int(time.time()),  # エラー発生時のタイムスタンプ
        }
        # 保存を行う
        AIAnalysisLog.objects.create(**log_data)

        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
