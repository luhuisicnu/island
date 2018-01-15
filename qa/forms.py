from django import forms

from .models import Question, QuestionImage, Answer, AnswerImage


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'description', 'type']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }


class QuestionImageForm(forms.ModelForm):
    class Meta:
        model = QuestionImage
        fields = ['image', 'question']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'content', 'user']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }


class AnswerImageForm(forms.ModelForm):
    class Meta:
        model = AnswerImage
        fields = ['image', 'answer']
