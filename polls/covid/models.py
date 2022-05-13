import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Вопрос")
    pub_date = models.DateTimeField(verbose_name="Дата публикации",
                                    default=datetime.datetime.now())
    is_active = models.BooleanField(verbose_name="Опубликован", default=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, verbose_name="Ответы")
    votes = models.IntegerField(verbose_name="Голосов", default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'
