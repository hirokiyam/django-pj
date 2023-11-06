from django.urls import path
from .views import home_view, save_response

urlpatterns = [
    path('', home_view, name='home'),
    path('save_response/', save_response, name='save_response'),
]
