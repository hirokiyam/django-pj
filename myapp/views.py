from django.shortcuts import render
from django.http import HttpResponse

# views.py
import requests
from django.http import JsonResponse
from .models import AIAnalysisLog # 保存するモデルをインポート

def home_view(request):
    return HttpResponse('')

def save_response(request):
    # URLのベース
    url = "http://example.com/"
    data = {
        "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"
    }
    print("--------------------------------デバッグ--------------------------------")

    try:
        # サードパーティAPIへPOSTリクエストを送信
        response = requests.post(url, data=data)

        # レスポンスが成功かチェック (200 OK)
        if response.status_code == 200:
            data = response.json()  # JSONデータを取得

            # 受け取ったレスポンスを保存するためのモデルインスタンスを作成
            api_response = AIAnalysisLog(
                content=data,  # あるいはdata['key']のように具体的なデータを指定
                # その他のモデルフィールドに必要な情報を設定
            )
            api_response.save()  # データベースに保存

            return JsonResponse({'status': 'success', 'message': 'API response saved successfully.'})

        else:
            # APIからエラーが返ってきた場合
            return JsonResponse({'status': 'error', 'message': 'Third-party API error.'}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        # リクエストに失敗した場合
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
