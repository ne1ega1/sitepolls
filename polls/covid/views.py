from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import ListView, TemplateView, CreateView
from django.views import View
from django.utils.regex_helper import Choice
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.template.response import TemplateResponse
from .models import *


class IndexView(ListView):
    template_name = 'covid/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone
                               .now()).order_by('pub_date')[:5]


class DetailsView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if UserVote.objects.select_related('choice')\
                           .filter(user=request.user, choice__question_id=question_id).exists():
            choices = question.choice_set.annotate(votes_count=Count('uservote'))
            user_choice = Choice.objects.filter(question_id=question_id, id__in=request.user.uservote_set
                                        .values_list('choice_id', flat=True)).first()
            return TemplateResponse(request, 'covid/results.html',
                                    {'question': question,
                                     'choices': choices,
                                     'error_message': f'Вы уже выбрали ответ "{user_choice}",\
                                      выберите другой вопрос или проголосуйте заново'})
        else:
            return TemplateResponse(request, 'covid/detail.html', {'question': question})


class ResultsView(TemplateView):
    model = Question
    template_name = 'covid/results.html'


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'covid/register.html'
    success_url = reverse_lazy('covid:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('covid:index')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'covid/login.html'


class LogoutUser(LogoutView):
    template_name = 'covid/index.html'


class Vote(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        choice_id = request.POST.get('choice')
        if choice_id is None:
            return TemplateResponse(request, 'covid/detail.html',
                                            {'question': question,
                                             'error_message': "Вы не сделали выбор"})
        else:
            UserVote.objects.create(user=request.user, choice_id=choice_id)
        choices = question.choice_set.annotate(votes_count=Count('uservote'))
        return TemplateResponse(request, 'covid/results.html',
                                        {'question': question,
                                         'choices': choices})


class CancelVote(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        UserVote.objects.select_related('choice') \
                        .filter(user=request.user, choice__question_id=question_id).delete()
        return TemplateResponse(request, 'covid/detail.html', {'question': question})
