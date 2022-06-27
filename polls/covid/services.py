import datetime
from django.db.models import Count
from django.shortcuts import get_object_or_404
from covid.models import Question, UserVote, Choice


def get_first_five_question():
    """ Возвращает QuerySet из первых 5 вопросов """
    queryset = Question.objects.filter(pub_date__lte=datetime.datetime.now()).order_by('pub_date')[:5]
    return queryset


def get_question(question_id: int):
    """ Возвращает выбранный вопрос """
    question = get_object_or_404(Question, pk=question_id)
    return question


def check_user_vote(request, question_id: int) -> bool:
    """ Проверяет, отвечал ли пользователь на данный вопрос """
    result_check = UserVote.objects.select_related('choice').filter(user=request.user, choice__question_id=question_id).exists()
    return result_check


def get_count_choices(question_id: int) -> int:
    """ Подсчитывает кол-во голосов за каждый выбор """
    choices = get_question(question_id).choice_set.annotate(votes_count=Count('uservote'))
    return choices


def get_user_choice(request, question_id: int):
    """ Возвращает выбор, который сделал пользователь """
    user_choice = Choice.objects.filter(question_id=question_id, id__in=request.user.uservote_set.values_list('choice_id', flat=True)).first()
    return user_choice


def create_user_vote(request, choice_id: int) -> None:
    """ Создает запись о выборе пользователя """
    UserVote.objects.create(user=request.user, choice_id=choice_id)


def delete_user_vote(request, question_id: int) -> None:
    """ Удаляет запись о выборе пользователя """
    UserVote.objects.select_related('choice') \
        .filter(user=request.user, choice__question_id=question_id).delete()
