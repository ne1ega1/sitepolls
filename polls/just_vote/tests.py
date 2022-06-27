import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() должен вернуть False, если время в pub_date в будущем """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() вернет False для вопросов, у которых pub_date более 1 дня назад """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ was_published_recently() вернет True для вопросов, у которых pub_date в течение последних суток """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Создать вопрос с заданным `question_text` и опубликовать
    заданное количество дней со смещением по настоящее время (отрицательно для вопросов, опубликованных
    в прошлом и положительно для вопросов, которые еще не опубликованы).
    """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ Если вопросов нет, отображается следующее: """
        response = self.client.get(reverse('just_vote:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет вопросов для голосования")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ Вопросы с датой публикации в прошлом отображаются на index.html """
        question = create_question(question_text="Вопрос в прошлом", days=-30)
        response = self.client.get(reverse('just_vote:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],)

    def test_future_question(self):
        """ Вопросы с  pub_date в будущем не отображаются на index.html """
        create_question(question_text="Вопрос в будущем", days=30)
        response = self.client.get(reverse('just_vote:index'))
        self.assertContains(response, "Нет вопросов для голосования")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """ Если существуют вопросы и в прошлом, и в будущем, отображаются только те что в прошлом """
        question = create_question(question_text="Вопрос в прошлом", days=-30)
        create_question(question_text="Вопрос в будущем", days=30)
        response = self.client.get(reverse('just_vote:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],)

    def test_two_past_questions(self):
        """ На index.html может отображаться несколько вопросов """
        question1 = create_question(question_text="Вопрос в прошлом 1.", days=-30)
        question2 = create_question(question_text="Вопрос в прошлом 2.", days=-5)
        response = self.client.get(reverse('just_vote:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """ DetailView вопросов с pub_date в будущем вернет ошибку 404 """
        future_question = create_question(question_text='Вопрос в будущем', days=5)
        url = reverse('just_vote:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ DetailView вопросов с pub_date в прошлом вернет текст вопроса """
        past_question = create_question(question_text='Вопрос в прошлом', days=-5)
        url = reverse('just_vote:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
