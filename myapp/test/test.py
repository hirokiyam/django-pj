from django.test import TestCase
from unittest.mock import patch
from myapp.views import save_response

class ExternalAPITests(TestCase):
    
    @patch('myapp.views.requests.get')  # requests.getをモックします
    def test_external_api_call(self, mock_get):
        # モックオブジェクトに対するレスポンスを設定
        mock_get.return_value.json.return_value = {
            "success": True,
            "message": "success",
            "estimated_data": {
                "class": 3,
                "confidence": 0.8683
            }
        }
        
        # モックされたレスポンスを使ってビューをテスト
        response = save_response()
        self.assertEqual(response['estimated_data']['class'], 3)

# 実行コマンド
# docker compose run web python manage.py test myapp.test.test.ExternalAPITests

# DBに許可を出す
# mysql -u django -p
# pass:django
# GRANT ALL PRIVILEGES ON *.* TO 'django'@'%';
# FLUSH PRIVILEGES;
