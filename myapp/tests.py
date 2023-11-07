from django.test import TestCase, RequestFactory
from unittest.mock import patch
from myapp.views import save_response
import json

class ExternalAPITests(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()

    @patch('myapp.views.requests.post')
    def test_external_api_call(self, mock_post):
        # モックオブジェクトに対するレスポンスを設定
        mock_post.return_value.json.return_value = {
            "success": True,
            "message": "Processed successfully",
            "estimated_data": {
                "class": 3,
                "confidence": 0.8683
            }
        }
        mock_post.return_value.status_code = 200

        
        # テスト用のリクエストを作成
        request_data = json.dumps({
            'image_path': '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg'
        })

        request = self.factory.post('/save_response', request_data, content_type='application/json')
        
        # モックされたレスポンスを使ってビューをテスト
        response = save_response(request)

        # ステータスコードとレスポンスデータを検証
        self.assertEqual(response.status_code, 200)

        # JsonResponseのcontentをデコードしてJSONとして解析
        response_data = json.loads(response.content.decode('utf-8'))
        
        # レスポンスデータを検証
        self.assertEqual(response_data['status'], "success")
        self.assertEqual(response_data['message'], "API response saved successfully.")

# 実行コマンド
# docker compose run web python manage.py test myapp.tests.ExternalAPITests

# DBに許可を出す
# mysql -u django -p
# pass:django
# GRANT ALL PRIVILEGES ON *.* TO 'django'@'%';
# FLUSH PRIVILEGES;
