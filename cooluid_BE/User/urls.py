from django.urls import path
from .views import SendMailSignUp, SendMailSignIn, RegisterView, CreatePostView
from . import views

urlpatterns = [
    path('get_email/', views.get_email_by_code, name='get_email_by_code'),
    path("register/", RegisterView.as_view(), name="register"),
    # path("check_login/", views.check_login_status, name="check_login_status"),
    path('sign_in/', SendMailSignIn.as_view(), name='sign_in'),
    path('sign_up/', SendMailSignUp.as_view(), name='sign_up'),
    path('email_signin/', views.email_signin, name='email_signin'),
    path('check_session/', views.check_session, name='check_session'),
    path('logout/', views.logout_view, name='logout'),
    path('search_movie/', views.search_movie, name='search_movie'),
    path('post_create/', CreatePostView.as_view(), name='create-post'),
    path('posts/', views.get_posts, name='get_posts'),
]