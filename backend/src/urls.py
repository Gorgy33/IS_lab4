from backend.src.views.auth_views import Login, Logout
from backend.src.views.user_views import GetUsers, SaveUser, AddUser, CreateUser
from backend.src.views.common_views import Base


def link_urls(app):
    app.add_url_rule("/",
                     view_func=Login.as_view(name='logon'),
                     methods=['GET'])

    app.add_url_rule("/login",
                     view_func=Login.as_view(name='login'),
                     methods=['POST'])

    app.add_url_rule("/logout",
                     view_func=Logout.as_view(name='logout'),
                     methods=['GET'])

    app.add_url_rule("/create_user",
                     view_func=CreateUser.as_view(name='create_user'),
                     methods=['GET'])

    app.add_url_rule("/users",
                     view_func=GetUsers.as_view(name='users'),
                     methods=['GET'])

    app.add_url_rule("/save_user",
                     view_func=SaveUser.as_view(name='save_user'),
                     methods=['POST'])

    app.add_url_rule("/add_user",
                     view_func=AddUser.as_view(name='add_user'),
                     methods=['GET'])

    app.add_url_rule("/index",
                     view_func=Base.as_view(name='index'),
                     methods=['GET'])
