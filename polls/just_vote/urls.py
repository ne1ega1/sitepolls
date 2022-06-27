from django.urls import path
from .views import IndexView, DetailsView, ResultsView, \
    Vote, CancelVote, RegisterUser, LoginUser, LogoutUser

app_name = 'just_vote'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:question_id>/', DetailsView.as_view(), name='detail'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', Vote.as_view(), name='vote'),
    path('<int:question_id>/cancel_vote/', CancelVote.as_view(), name='cancel_vote'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]
