from front.views.index import IndexView
from front.views.captcha import CaptchaView
from front.views.users import RegisterView
from front.views.users import LoginView
from front.views.users import LogoutView
from front.views.users import ShowPlayersView
from front.views.topics import TopicsView
from front.views.topics import TopicSingleView
from front.views.images import DockerOperationView
from front.views.flag import CheckFlagView
from front.views.rank import RankView
from front.views.personal import PersonalView

from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name="front_index"),
    path('captcha/', CaptchaView.as_view(), name="captcha"),
    path('reg', RegisterView.as_view(), name="front_reg"),
    path('login', LoginView.as_view(), name="front_login"),
    path('logout', LogoutView.as_view(), name="front_logout"),
    path('players', ShowPlayersView.as_view(), name="front_players"),
    path('topics', TopicsView.as_view(), name="front_topics"),
    path('topic/<str:topic_id>', TopicSingleView.as_view(), name="front_topic"),
    path('images', DockerOperationView.as_view(), name="front_operate"),
    path('flag', CheckFlagView.as_view(), name="front_flag"),
    path('score', RankView.as_view(), name="front_rank"),
    path('personal/<str:username>', PersonalView.as_view(), name="front_personal"),
]
