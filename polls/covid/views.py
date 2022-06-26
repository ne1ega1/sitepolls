from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import ListView, TemplateView, CreateView
from django.views import View
from django.template.response import TemplateResponse
from .services import *


class IndexView(ListView):
    """ Отображение списка вопросов на главной странице """
    template_name = 'covid/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        queryset = get_first_5_question()
        return queryset


class DetailsView(View):
    """ Отображение вариантов ответа на выбранный вопрос """
    def get(self, request, question_id):
        question = get_question(question_id)
        if check_user_vote(request, question_id) == True:
            choices = get_count_choices(question_id)
            user_choice = get_user_choice(request, question_id)
            return TemplateResponse(request, 'covid/results.html',
                                            {'question': question,
                                             'choices': choices,
                                             'error_message': f'Вы уже выбрали ответ "{user_choice}",\
                                              выберите другой вопрос или проголосуйте заново'})
        return TemplateResponse(request, 'covid/detail.html', {'question': question})


class ResultsView(TemplateView):
    """ Отображение результатов голосования """
    model = Question
    template_name = 'covid/results.html'


class RegisterUser(CreateView):
    """ Регистрация """
    form_class = UserCreationForm
    template_name = 'covid/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('covid:index')


class LoginUser(LoginView):
    """ Авторизация """
    form_class = AuthenticationForm
    template_name = 'covid/login.html'


class LogoutUser(LogoutView):
    """ Выход из авторизации """
    template_name = 'covid/index.html'


class Vote(View):
    """ Запись выбора пользователя в базу данных """
    def post(self, request, question_id):
        question = get_question(question_id)
        choice_id = request.POST.get('choice')
        if choice_id is None:
            return TemplateResponse(request, 'covid/detail.html',
                                            {'question': question,
                                             'error_message': "Вы не сделали выбор"})
        create_user_vote(request, choice_id)
        choices = get_count_choices(question_id)
        return TemplateResponse(request, 'covid/results.html',
                                        {'question': question,
                                         'choices': choices})


class CancelVote(View):
    """ Удаление выбора пользователя из базы данных """
    def post(self, request, question_id):
        question = get_question(question_id)
        delete_user_vote(request, question_id)
        return TemplateResponse(request, 'covid/detail.html', {'question': question})
