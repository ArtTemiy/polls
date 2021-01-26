from django.urls import path
from polling.api_views import *

urlpatterns = [
    path('poll', csrf_exempt(PollList.as_view()), name='polls'),
    path('poll/<int:pk>', PollDetail.as_view(), name='poll'),

    path('question', QuestionList.as_view(), name='questions'),
    path('question/<int:pk>', QuestionDetail.as_view(), name='question'),

    path('answer', AnswerList.as_view(), name='answers'),
    path('answer/<int:pk>', AnswerDetail.as_view(), name='answer'),

    path('result', ResultView.as_view(), name='results'),
    path('result/<int:id>', ResultDetail.as_view(), name='result'),
]
