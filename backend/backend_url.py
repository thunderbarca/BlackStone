from backend.views.index import IndexView
from backend.views.index import RegView
from backend.views.index import LogoutView
from backend.views.index import ChangeView
from backend.views.login import LoginView
from backend.views.apis import IndexAPIView
from backend.views.apis import UserApiView
from backend.views.welcome import WelcomeView
from backend.views.admins import UserView
from backend.views.admins import AddUserView
from backend.views.players import PlayersView
from backend.views.setting import SettingMenu
from backend.views.images import ImagesView
from backend.views.images import ImageAddView
from backend.views.players import PlayersAddView
from backend.views.apis import PlayersApiView
from backend.views.apis import ImagesApiView
from backend.views.category import CategoryView
from backend.views.category import CategoryAddView
from backend.views.category import CategoryEditView
from backend.views.apis import CategoryApiView
from backend.views.apis import ContainerApiView
from backend.views.apis import ResolverApiView
from backend.views.container import ContainerView
from backend.views.resolver import ResolverView
from backend.views.players import PlayersEditView
from backend.views.images import ImagesEditView
from backend.views.uploads import UploadView

from django.urls import path

urlpatterns = [
    path('index', IndexView.as_view(), name="back_index"),
    path('', IndexView.as_view(), name="back_index"),
    path('login', LoginView.as_view(), name="back_login"),
    path('logout', LogoutView.as_view(), name="back_logout"),
    path('welcome', WelcomeView.as_view(), name="back_welcome"),
    path('setting', SettingMenu.as_view(), name="back_setting"),
    path('players', PlayersView.as_view(), name="back_players"),
    path('change', ChangeView.as_view(), name="back_change"),

    # 管理用户相关路由
    path('user_show', UserView.as_view(), name="back_user"),
    path('add', AddUserView.as_view(), name="back_user_add"),
    path('user_api', UserApiView.as_view(), name="back_api_users"),

    # API相关
    path('index_api', IndexAPIView.as_view(), name="api_index"),
    # path('menu_api', MenuApiView.as_view(), name="api_menu"),

    # 镜像相关路由
    path('images_list', ImagesView.as_view(), name="back_images_show"),
    path('images_add', ImageAddView.as_view(), name="back_images_add"),
    path('images_api', ImagesApiView.as_view(), name="back_images_api"),
    path('images_edit/', ImagesEditView.as_view(), name="back_images_edit"),

    # 比赛用户相关路由
    path('players_show', PlayersView.as_view(), name="back_players"),
    path('players_add', PlayersAddView.as_view(), name="back_player_add"),
    path('players_api', PlayersApiView.as_view(), name="back_players_api"),
    path('players_edit/', PlayersEditView.as_view(), name="back_player_edit"),

    # 分类标签路由
    path('categorys_show', CategoryView.as_view(), name="back_category_show"),
    path('categorys_add', CategoryAddView.as_view(), name="back_category_add"),
    path('categorys_edit/', CategoryEditView.as_view(), name="back_category_edit"),
    path('categorys_api', CategoryApiView.as_view(), name="back_category_api"),

    # 容器相关路由
    path('container_show', ContainerView.as_view(), name="back_container_show"),
    path('container_api', ContainerApiView.as_view(), name="back_container_api"),

    # 题目相关路由
    path('resolver_show', ResolverView.as_view(), name="back_resolver_show"),
    path('resolver_api', ResolverApiView.as_view(), name="back_resolver_api"),

    # path('reg', RegView.as_view(), name="reg"),
    path('uploads', UploadView.as_view(), name="uploads"),
]
