from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("logout/", views.UserLogoutView.as_view()),
    path("token/access/", views.ObtainAccessToken.as_view()),
]
