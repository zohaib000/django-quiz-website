from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.home, name="home"),
    path("showTests", views.showTests.as_view(), name="showTests"),
    path("sendOutputData", views.sendOutputData, name="sendOutputData"),
    path("takeTest/<int:pk>", views.takeTest.as_view(), name="takeTest"),
    # ? authentication part
    path("user_login", views.user_login, name="user_login"),
    path("signup", views.signup, name="signup"),
    path("logo", views.logo, name="logo"),
    path("change_password", views.change_password, name="change_password"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("verify/<str:token_coming>/", views.verify, name="verify"),
    path("verifying/<str:token_coming>/", views.verifying, name="verifying"),
    ##jobs
    path("notifications", views.notify, name="notifications"),
    path("help", views.help, name="help"),
    ## ajax request
    path("password_reset", views.password_reset_request, name="password_reset"),
    ####chat
]
