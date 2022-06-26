import datetime
from django.conf import settings
from django.db import models


class Question(models.Model):
    """ Вопросы """
    question_text = models.CharField(max_length=200, verbose_name="Вопрос")
    pub_date = models.DateTimeField(verbose_name="Дата публикации", default=datetime.datetime.now())
    is_active = models.BooleanField(verbose_name="Опубликован", default=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = datetime.datetime.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    """ Ответы """
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, verbose_name="Ответы")

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'


class UserVote(models.Model):
    """ Выбранные ответы пользователей """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, verbose_name="Выбранный ответ", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user} - {self.choice.question}'

    class Meta:
        unique_together = [['user', 'choice']]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
