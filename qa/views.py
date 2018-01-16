import json

from django.shortcuts import render, get_object_or_404, redirect
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
        answers = AnswerModel.objects.filter(question=question).order_by('-created_time').all()
        form = AnswerForm()
        context = {'question': question, 'answers': answers, 'form': form}
        return render(request, 'qa/question.html', context=context)

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        question = get_object_or_404(QuestionModel, pk=kwargs.get('question_id'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.customize_user
            answer.save()
        return redirect('question', question_id=question.id)


class NewQuestion(View):
    def get(self, request):
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'qa/new_question.html', context=context)

    @method_decorator(login_required)
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.customize_user
            question.save()
            return redirect('question', question_id=question.id)

        context = {"form": form}
        return render(request, 'customize_auth/register.html', context=context)


class AnswerList(View):
    def get(self, request):
        question = get_object_or_404(int(request.GET.get('question_id', 0)))
        answers = AnswerModel.objects.filter(question=question).order_by('-created_time').all()
        answer_list = json.loads(serializers.serialize('json', answers))
        return JsonResponse({'count': len(answer_list), 'results': answer_list})


@method_decorator(login_required, name='dispatch')
class Approvals(View):
    def get(self, request):
        pass


@method_decorator(login_required, name='dispatch')
class Negations(View):
    def get(self, request):
        pass
