from django.contrib import admin
from django.db import models
from .models import *


# ? questions answers table


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "test_name",
        "test_image",
        "questions_file",
        "answers_file",
        "published_date",
    ]
    list_filter = ["published_date"]
    search_fields = ["test_name"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "test",
        "question_text",
        "option1",
        "option2",
        "option3",
        "option4",
    ]
    list_filter = ["test"]
    search_fields = ["question_text"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "answer_text", "correct_option"]
    list_filter = ["question__test"]
    search_fields = ["answer_text"]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "test_name",
        "total_questions",
        "correct_answers",
        "incorrect_answers",
        "score",
        "status",
    ]
    search_fields = ["user"]


# ?
# from .models import *
# Register your models here.
class email_verify_admin(admin.ModelAdmin):
    list_display = ["id", "user", "token", "is_verified"]


class user_details_admin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "second_name",
        "country",
        "country_code",
        "profile_image",
        "user",
    ]


class referals_admin(admin.ModelAdmin):
    list_display = ["promoter", "referal_user", "reward", "verified"]


class earnings_admin(admin.ModelAdmin):
    list_display = ["total", "user", "spent_on_jobs", "deposit"]


class jobs_admin(admin.ModelAdmin):
    list_display = [
        "job_id",
        "job_title",
        "job_description",
        "overall_price",
        "job_price_per",
        "feature_price",
        "user_posted",
        "date_time_when_posted",
        "total_conversions",
        "done_conversions",
        "category",
        "sub_category",
        "posted_from",
        "country",
        "allowed_countries",
    ]


class jobs_proofs_admin(admin.ModelAdmin):
    list_display = [
        "id",
        "job_id",
        "user_submitted_job",
        "proof1",
        "proof2",
        "proof3",
        "proof4",
        "job_earning",
        "status",
        "posted_by",
    ]


class notifications_admin(admin.ModelAdmin):
    list_display = ["id", "title", "url", "bell_digit", "to_user", "date", "unseen"]


class payment_history_admin(admin.ModelAdmin):
    list_display = ["user", "TID", "payment_account", "payment_proof"]


class contacts_admin(admin.ModelAdmin):
    list_display = ["email", "whatsapp", "subject", "message"]


class withdraw_admin(admin.ModelAdmin):
    list_display = [
        "user",
        "amount_to_withdraw",
        "payment_method",
        "payment_account_info",
        "status",
        "paid_on",
    ]


# @admin.register(categories)
# class categories_admin(admin.ModelAdmin):
#     list_display = ["id", "name"]


# @admin.register(subcategories)
# class subcategories_admin(admin.ModelAdmin):
#     list_display = ["id", "name", "belongs_to"]


# @admin.register(fake_proof_reports)
# class fake_proof_reports_admin(admin.ModelAdmin):
#     list_display = ["job_id", "proof_id", "user_submitted_job", "reason", "job_owner"]


# @admin.register(chat_data)
# class chat_data_admin(admin.ModelAdmin):
#     list_display = ["user", "message"]


# @admin.register(posts)
# class posts_admin(admin.ModelAdmin):
#     list_display = ["title"]


admin.site.register(email_verify, email_verify_admin)
admin.site.register(user_details, user_details_admin)
# admin.site.register(referals, referals_admin)
# admin.site.register(earnings, earnings_admin)
# admin.site.register(jobs, jobs_admin)
# admin.site.register(jobs_proofs, jobs_proofs_admin)
# admin.site.register(notifications, notifications_admin)
# admin.site.register(payment_history, payment_history_admin)
# admin.site.register(contacts, contacts_admin)
# admin.site.register(withdraw, withdraw_admin)
