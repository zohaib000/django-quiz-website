from django.utils.encoding import force_bytes, force_str
from unicodedata import category
from django.db.models import Q, F
from email.policy import EmailPolicy
from http.client import HTTPResponse
from faker import Faker
import requests
from django.views.decorators.csrf import csrf_exempt
from aiohttp import http
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
import re
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.models import User
import datetime
import pendulum
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from home.models import *
from home.forms import RegisterForm
from datetime import time
import os
from datetime import datetime
import random
from datetime import date
from home.forms import Postform
import uuid
from django.contrib import messages
import math
from django.conf import settings
from django.core.mail import send_mail
from PIL import Image
from django.conf import settings

from pc.settings import BASE_DIR
from django.http import JsonResponse
from .models import jobs

from email.mime import multipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.views import View
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404


# class Result(models.Model):
#     user = models.CharField(max_length=500)
#     total_questions = models.CharField(max_length=500)
#     correct_answers = models.CharField(max_length=500)
#     incorrect_answers = models.CharField(max_length=500)
#     score = models.CharField()  # correct_answers/total_answers

#     def __str__(self):
#         return self.user


@csrf_exempt
def sendOutputData(request):
    if request.method == "POST":
        quiz_data = request.POST.get("result")
        data = json.loads(quiz_data)
        user = request.user

        selected_test = data["selectedTest"]
        print(data)
        correct_answers = 0
        incorrect_answers = 0
        total_questions = len(data.items())
        for key, value in data.items():
            if key != "selectedTest":
                question = Question.objects.get(id=key)
                correct_option = Answer.objects.get(question=question).correct_option
                print(question.question_text)
                if value == correct_option:
                    print("correct answer")
                    correct_answers = correct_answers + 1
                else:
                    print("incorrect answer")
                    incorrect_answers = incorrect_answers + 1

        test_name = Test.objects.filter(id=selected_test)[0].test_name
        # Calculate percentage
        percentage = (correct_answers / total_questions) * 100

        # Determine status
        status = "Pass" if percentage >= 35 else "Fail"

        Result.objects.create(
            user=request.user,
            test_name=test_name,
            total_questions=total_questions,
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
            score=percentage,
            status=status,
        )
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


# related to tests
class showTests(View):
    def get(self, request):
        if request.user.is_authenticated:

            tests = Test.objects.all()

            logged_user = user_details.objects.filter(user=request.user)
            index = len(logged_user) - 1
            logged_user = logged_user[index]

            ### getting job info
            context = {"user": logged_user, "tests": tests}
            return render(request, "home/showTests.html", context)

        else:
            return render(request, "landing/index.html")

    def post(self, request):
        pass


# related to tests
class takeTest(View):
    def get(self, request, pk):
        if request.user.is_authenticated:

            # logic to send all questions and answers to user for passing text
            logged_user = user_details.objects.filter(user=request.user)
            index = len(logged_user) - 1
            logged_user = logged_user[index]

            ### getting questions data
            questions = Question.objects.filter(test=pk)
            questions_data = list(questions.values())

            context = {"user": logged_user, "questions": questions_data}
            print(context)
            return render(request, "home/takeTest.html", context)

        else:
            return render(request, "landing/index.html")

    def post(self, request):
        pass


msg = MIMEMultipart()


def send_email(subject, template, email):
    with open(template, "r") as f:
        html = f.read()
        FROM = "fablyteam@gmail.com"
        PASS = "vvpyklnooevpzgbs"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, PASS)
        message = f"Subject: {subject}\nFrom: {FROM}\nTo: {email} \nContent-Type: text/html\n\n {html}"
        server.sendmail(FROM, email, message)
        server.close()


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "home/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "fableey.com",
                        "site_name": "Fableey",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "https",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "admin@example.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")

    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="home/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


def home(request):
    if request.user.is_authenticated:
        logged_user = user_details.objects.filter(user=request.user)
        index = len(logged_user) - 1
        logged_user = logged_user[index]

        total_tests = Result.objects.filter(user=request.user).count()
        passed_tests = Result.objects.filter(user=request.user, status="pass").count()
        failed_tests = Result.objects.filter(user=request.user, status="fail").count()
        avg_score = None
        try:
            avg_score = int(passed_tests / total_tests) * 100
        except:
            avg_score = 0
        user_tests = Result.objects.filter(user=request.user)
        print(passed_tests, failed_tests)

        ### getting job info

        context = {
            "user": logged_user,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "avg_score": avg_score,
            "tests": user_tests,
        }
        return render(request, "home/index.html", context)
    else:
        return render(request, "landing/index.html")
    return render(request, "landing/index.html")


def signup(request):
    if request.method == "POST":
        reg_user = request.POST.get("username")
        reg_email = request.POST.get("email")
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            fm.save()
            email_token = str(uuid.uuid4())
            data = email_verify(user=reg_user, token=email_token)
            data.save()
            subject = "Verify your Email to Login into Fableey!"
            message = f"Hi {reg_user},\n Thank you for registering in Fableey ,the world largest investing and earning platform.\n You can get your projects Done easily with Huge traffic of Fableey.\n As you have become member of Fableey. Now it is time to Verify your account to get Started. \n \n \n Click on Link to verify your account.  https://fableey.com/verify/{email_token}/ \n \n Regards. \n Fableey team!"
            msg = MIMEMultipart()
            msg["From"] = "fablyteam@gmail.com"
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))
            server = smtplib.SMTP("smtp.gmail.com: 587")
            server.starttls()
            server.login("fablyteam@gmail.com", "vvpyklnooevpzgbs")
            server.sendmail("fablyteam@gmail.com", reg_email, msg.as_string())
            server.quit()
            ### saving profile data
            data2 = user_details(
                first_name="Daniel",
                second_name="Baryan",
                email_adress=reg_email,
                user=reg_user,
                country_code="pk",
                country="pakistan",
                profile_image="profile pics/demo_profile.png",
            )
            data2.save()
            earnings(total=0, spent_on_jobs=0, deposit=0, user=reg_user).save()
            messages.success(
                request,
                "Your Account has been created successfully!.Check your Email to verify your Account!",
            )
            return HttpResponseRedirect("/user_login")
    else:
        fm = RegisterForm()
        return render(request, "home/signup.html", {"form": fm})
    return render(request, "home/signup.html", {"form": fm})


def user_login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data["username"]
            upass = fm.cleaned_data["password"]
            user = authenticate(username=uname, password=upass)
            if user is not None:
                log_user = email_verify.objects.filter(user=uname).latest("id")
                if log_user.is_verified:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return render(
                        request,
                        "home/login.html",
                        {
                            "form": fm,
                            "error": "We have sent you a confirmation Email,Please verify your Email to Login.",
                            "diplay": "block",
                        },
                    )

    else:
        fm = AuthenticationForm()
        return render(request, "home/login.html", {"form": fm})
    return render(request, "home/login.html", {"form": fm})


def logo(request):
    logout(request)
    return HttpResponseRedirect("/user_login")


def verify(request, token_coming):
    obj = email_verify.objects.get(token=token_coming)
    obj.is_verified = True
    obj.save()
    return render(request, "home/verification_success.html")


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fname = request.POST.get("fname")
            sname = request.POST.get("sname")
            country_code = request.POST.get("country_code")
            country_name = request.POST.get("country_name")
            img = request.FILES.get("file")
            Email_id = User.objects.get(username=request.user).email
            data = user_details(
                first_name=fname,
                second_name=sname,
                country_code=country_code,
                country=country_name,
                user=request.user,
                email_adress=Email_id,
                profile_image=img,
            )
            data.save()
            messages.success(request, "Profile Updated successfully!")
            return HttpResponseRedirect("/")

        else:
            records = withdraw.objects.filter(user=request.user)
            logged_user = user_details.objects.filter(user=request.user)
            index = len(logged_user) - 1
            logged_user = logged_user[index]
            return render(
                request, "home/settings.html", {"user": logged_user, "records": records}
            )
    else:
        return HttpResponseRedirect("user_login")


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, "Password Updated sucessfully!")
                return HttpResponseRedirect("/")

        else:
            fm = PasswordChangeForm(user=request.user)
            logged_user = user_details.objects.filter(user=request.user)
            index = len(logged_user) - 1
            logged_user = logged_user[index]
            return render(
                request, "home/change_pass.html", {"form": fm, "user": logged_user}
            )
        logged_user = user_details.objects.filter(user=request.user)
        index = len(logged_user) - 1
        logged_user = logged_user[index]
        return render(
            request, "home/change_pass.html", {"form": fm, "user": logged_user}
        )
    else:
        return HttpResponseRedirect("user_login")


def verifying(request, token_coming):
    obj = email_verify.objects.get(token=token_coming)
    obj.is_verified = True
    obj.save()
    return render(request, "home/verification_success_referal.html")


def notify(request):
    if request.user.is_authenticated:
        logged_user = user_details.objects.filter(user=request.user)
        index = len(logged_user) - 1
        logged_user = logged_user[index]
        user_notifications = notifications.objects.filter(to_user=request.user)
        total = len(notifications.objects.filter(to_user=request.user)) + len(
            notifications.objects.filter(to_user="all")
        )
        all_notifications = notifications.objects.filter(
            Q(to_user="all") | Q(to_user=request.user)
        )

        ##saving unseen False
        for j in user_notifications:
            j.unseen = False
            j.save()
        return render(
            request,
            "home/notify.html",
            {
                "user": logged_user,
                "all_notifications": all_notifications,
                "total": total,
            },
        )
    else:
        return HttpResponseRedirect("user_login")


def help(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            sub = request.POST.get("subject")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            data = contacts(subject=sub, email=email, whatsapp=phone, message=message)
            data.save()
            return render(request, "home/message_success.html")
        else:
            logged_user = user_details.objects.filter(user=request.user)
            index = len(logged_user) - 1
            logged_user = logged_user[index]
            return render(request, "home/help.html", {"user": logged_user})
        logged_user = user_details.objects.filter(user=request.user)
        index = len(logged_user) - 1
        logged_user = logged_user[index]
        return render(request, "home/help.html", {"user": logged_user})
    else:
        return HttpResponseRedirect("/user_login")
