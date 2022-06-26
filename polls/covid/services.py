from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from covid.models import Question, UserVote, Choice


def get_list_of_question():
    queryset = Question.objects.filter(pub_date__lte=timezone
                               .now()).order_by('pub_date')[:5]
    return queryset


def get_question(question_id):
    question = get_object_or_404(Question, pk=question_id)
    return question


def check_user_vote(request, question_id):
    result_check = UserVote.objects.select_related('choice') \
                                   .filter(user=request.user, choice__question_id=question_id) \
                                   .exists()
    return result_check


def get_count_choices(question_id):
    choices = get_question(question_id).choice_set.annotate(votes_count=Count('uservote'))
    return choices


def get_user_choice(request, question_id):
    user_choice = Choice.objects.filter(question_id=question_id, id__in=request.user.uservote_set
                                .values_list('choice_id', flat=True))\
                                .first()
    return user_choice


def create_user_vote(request, choice_id):
    UserVote.objects.create(user=request.user, choice_id=choice_id)


def delete_user_vote(request, question_id):
    UserVote.objects.select_related('choice') \
        .filter(user=request.user, choice__question_id=question_id).delete()
