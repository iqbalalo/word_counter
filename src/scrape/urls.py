from django.urls import path

from .views import WordCountView

urlpatterns = [
    path('wordcount/', WordCountView.as_view(), name='wordcount'),
]
