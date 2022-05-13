from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.regex_helper import Choice
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.utils import timezone


class IndexView(ListView):
    template_name = 'covid/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('pub_date')[:5]


class DetailsView(DetailView):
    model = Question
    template_name = 'covid/detail.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now())


class ResultsView(DetailView):
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


def logout_user(request):
    logout(request)
    return redirect('covid:index')


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'covid/detail.html', {
            'question': question,
            'error_message': "Вы не сделали выбор",
        })
    else:
        request.session['choice'] = selected_choice.id
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('covid:results', args=(question.id,)))


def cancel_vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    selected_choice = question.choice_set.get(pk=request.session['choice'])
    selected_choice.votes -= 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('covid:detail', args=(question.id,)))