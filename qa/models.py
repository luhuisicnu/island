from django.db import models
from customize_auth.models import User


class Question(models.Model):
    subject = models.CharField(max_length=255, unique=True, verbose_name='提问标题')
    description = models.TextField(verbose_name='提问描述')
    type = models.CharField(max_length=40, verbose_name='问题类型')
    solved = models.BooleanField(default=False, verbose_name='解决状态')
    disabled = models.BooleanField(default=False, verbose_name='禁用')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    first_answer = models.OneToOneField('Answer', related_name='acception_as_first',
                                        null=True, on_delete=models.SET_NULL)
    best_answer = models.OneToOneField('Answer', related_name='acception_as_best',
                                       null=True, on_delete=models.SET_NULL)


class Answer(models.Model):
    content = models.TextField(verbose_name='回答内容')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    disabled = models.BooleanField(default=False, verbose_name='禁用')
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    approvals = models.ManyToManyField(User, related_name='approval_answer')
    negations = models.ManyToManyField(User, related_name='negation_answer')

    @property
    def acception(self):
        if hasattr(self, 'acception_as_first') or hasattr(self, 'acception_as_best'):
            return True
        return False


class QuestionImage(models.Model):
    image = models.ImageField(upload_to='question')
    question = models.ForeignKey('Question', related_name='images', on_delete=models.CASCADE)


class AnswerImage(models.Model):
    image = models.ImageField(upload_to='answer')
    answer = models.ForeignKey('Answer', related_name='images', on_delete=models.CASCADE)
