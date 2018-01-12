import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core import serializers

from customize_auth.login_management import login_required
from .models import Question as QuestionModel, Answer as AnswerModel
from .forms import QuestionForm, QuestionImageForm, AnswerForm, AnswerImageForm


class QuestionList(View):
    def get(self, request):
        questions = QuestionModel.objects.order_by('-id').all()
        context = {'questions': questions}
        return render(request, 'qa/question_list.html', context=context)


class Question(View):
    def get(self, request, **kwargs):
        question = get_object_or_404(QuestionModel, pk=kwargs.get('question_id'))
        context = {'question': question}
        return render(request, 'qa/question.html', context=context)

    @method_decorator(login_required)
    def post(self, request):
        pass


class AnswerList(View):
    def get(self, request):
        question = get_object_or_404(int(request.GET.get('question_id', 0)))
        answers = AnswerModel.objects.filter(question=question).order_by('-created_time').all()
        answer_list = json.loads(serializers.serialize('json', answers))
        return JsonResponse({'count': len(answer_list), 'results': answer_list})


class Answer(View):
    def get(self, request, **kwargs):
        question = get_object_or_404(QuestionModel, pk=kwargs.get('answer_id'))
        question = json.loads(serializers.serialize('json', [question, ]))[0]
        return JsonResponse(question)

    @method_decorator(login_required)
    def post(self, request):
        pass


@method_decorator(login_required, name='dispatch')
class Approvals(View):
    def get(self, request):
        pass


@method_decorator(login_required, name='dispatch')
class Negations(View):
    def get(self, request):
        pass
