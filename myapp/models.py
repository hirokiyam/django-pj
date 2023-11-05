from django.db import models

class AIAnalysisLog(models.Model):
    image_path = models.CharField(max_length=255, blank=True, null=True)
    success = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    class_field = models.IntegerField(db_column='class', blank=True, null=True)  # `class`はPythonの予約語なのでfield名として使うことはできません。`db_column`を使用して実際のデータベースのカラム名を指定します。
    confidence = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    request_timestamp = models.PositiveIntegerField(blank=True, null=True)
    response_timestamp = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ai_analysis_log'

    def __str__(self):
        return f'{self.id} - {self.image_path}'

# docker compose run web python manage.py makemigrations
# docker compose run web python manage.py migrate

