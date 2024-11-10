from django.urls import path
from .views import SignUpView, logout
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", logout, name="logout"),
]