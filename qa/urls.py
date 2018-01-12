from django.urls import path
from .views import QuestionList, Question, AnswerList, Answer

urlpatterns = [
    path('questions/', QuestionList.as_view(), name='question_list'),
    path('questions/<int:question_id>/', Question.as_view(), name='question'),
    path('answers/', AnswerList.as_view(), name='answer_list'),
    path('answers/<int:answer_id>', Answer.as_view(), name='answer'),
]

