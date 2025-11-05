import email
from email.policy import default
from django.db import models
from django.http import request
from PIL import Image
from ckeditor.fields import RichTextField
from django import forms


# questions ,anaswers and test tables

from django.db import models


import json


def Extract_Answers(file_path):
    answers_data = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for idx, line in enumerate(lines, start=1):
            line = line.strip()
            option = line.split(".")[1].strip().upper()
            # Construct answer data
            answer_data = {"question_id": idx, "option": option}
            answers_data.append(answer_data)

    return json.dumps(answers_data, indent=4)


# Function to extract question & Options  from text file
# def Extract_Questions_Options(file_path):
#     with open(file_path, "r") as file:
#         lines = file.readlines()

#     # Initialize variables
#     qa_pairs = []
#     question = ""
#     options = []

#     # Iterate through each line in the file
#     for line in lines:
#         line = line.strip()
#         if line == "":
#             # End of options, construct question-answer pair
#             qa_data = {
#                 "question": question,
#                 "option1": options[0],
#                 "option2": options[1],
#                 "option3": options[2],
#                 "option4": options[3],
#             }
#             qa_pairs.append(qa_data)
#             question = ""  # Reset question
#             options = []  # Reset options for the next question
#         elif line.startswith(("A.", "B.", "C.", "D.")):
#             # Add options without option names
#             options.append(line[3:])
#         else:
#             # Add to the current question
#             question += " " + line

#     json_data = json.dumps(qa_pairs, indent=4)
#     return json_data


def Extract_Questions_Options(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Initialize variables
    qa_pairs = []
    question = ""
    options = []

    # Iterate through each line in the file
    for line in lines:
        line = line.strip()
        if line == "":
            # End of options, construct question-answer pair
            if question and len(options) == 4:  # Only add if we have question and 4 options
                qa_data = {
                    "question": question.strip(),
                    "option1": options[0],
                    "option2": options[1],
                    "option3": options[2],
                    "option4": options[3],
                }
                qa_pairs.append(qa_data)
            question = ""  # Reset question
            options = []  # Reset options for the next question
        elif line.startswith(("A.", "B.", "C.", "D.")):
            # Add options without option names
            options.append(line[3:])
        else:
            # Add to the current question
            question += " " + line

    # ADD THIS: Handle the last question (no empty line after it)
    if question and len(options) == 4:
        qa_data = {
            "question": question.strip(),
            "option1": options[0],
            "option2": options[1],
            "option3": options[2],
            "option4": options[3],
        }
        qa_pairs.append(qa_data)

    json_data = json.dumps(qa_pairs, indent=4)
    return json_data


class Test(models.Model):
    test_name = models.CharField(max_length=255)
    test_image = models.ImageField(
        upload_to="test_images/", default="/test_images/default.png"
    )
    questions_file = models.FileField(upload_to="questions_files/")
    answers_file = models.FileField(upload_to="answers_files/")
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name

    def save(self, *args, **kwargs):
        super(Test, self).save(*args, **kwargs)
        if self.questions_file:
            questions_file_path = self.questions_file.path
            answers_file_path = self.answers_file.path
            questions_data = Extract_Questions_Options(questions_file_path)
            answers_data = Extract_Answers(answers_file_path)
            print(questions_data, answers_data)
            self.load_questions_answers(questions_data, answers_data)

    def load_questions_answers(self, questions_data, answers_data):
        questions = json.loads(questions_data)  # dict format
        answers = json.loads(answers_data)  # dict format
        print(answers)
        for idx, q_data in enumerate(questions):
            question_text = q_data.get("question", "")
            option1 = q_data.get("option1", "")
            option2 = q_data.get("option2", "")
            option3 = q_data.get("option3", "")
            option4 = q_data.get("option4", "")
            # Create Question object
            question = Question.objects.create(
                test=self,
                question_text=question_text,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
            )
            correct_option = str(answers[idx]["option"]).lower()
            answer_text = None
            if correct_option == "a":
                answer_text = option1
            elif correct_option == "b":
                answer_text = option2
            elif correct_option == "c":
                answer_text = option3
            elif correct_option == "d":
                answer_text = option4
            Answer.objects.create(
                question=question,
                answer_text=answer_text,
                correct_option=correct_option,
            )


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, related_name="answer"
    )
    answer_text = models.TextField()  # correct answer text "Programming Language"
    correct_option = models.CharField(max_length=300)  # correct answer option like "D"

    def __str__(self):
        return self.question.question_text


class Result(models.Model):
    user = models.CharField(max_length=500)
    test_name = models.CharField(max_length=500)
    total_questions = models.CharField(max_length=500)
    correct_answers = models.CharField(max_length=500)
    incorrect_answers = models.CharField(max_length=500)
    score = models.CharField(max_length=500)  # correct_answers/total_answers
    status = models.CharField(max_length=500)

    def __str__(self):
        return self.user


#  other tables


# Create your models here.
class posts(models.Model):
    slug = models.SlugField()
    image = models.ImageField(upload_to="Articles Feature Images")
    title = models.CharField(max_length=5000)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    content = RichTextField()

    def __str__(self):
        return self.title


class email_verify(models.Model):
    user = models.CharField(max_length=2000)
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)


class user_details(models.Model):
    first_name = models.CharField(max_length=130)
    second_name = models.CharField(max_length=130)
    user = models.CharField(max_length=124, default="No info")
    email_adress = models.CharField(max_length=300, default="No Email")
    country = models.CharField(max_length=130)
    country_code = models.CharField(max_length=1200)
    profile_image = models.ImageField(upload_to="profile pics")

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.profile_image.path)  # Open image using self
        new_img = (500, 800)
        img.thumbnail(new_img)
        img.save(self.profile_image.path)


class referals(models.Model):
    promoter = models.CharField(max_length=2000)
    referal_user = models.CharField(max_length=2000)
    reward = models.CharField(max_length=2000)
    verified = models.BooleanField(default=False)


class earnings(models.Model):
    total = models.FloatField()
    user = models.CharField(max_length=2000)
    spent_on_jobs = models.FloatField()
    deposit = models.FloatField()


class jobs(models.Model):
    user_posted = models.CharField(max_length=100)
    job_id = models.CharField(max_length=500)
    date_time_when_posted = models.CharField(
        max_length=200
    )  # print(pendulum.now().to_formatted_date_string())
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    job_price_per = models.FloatField()
    overall_price = models.FloatField()
    total_conversions = models.IntegerField()
    done_conversions = models.IntegerField()
    proof1 = models.CharField(max_length=5000)
    proof1_type = models.CharField(max_length=200)
    proof2 = models.CharField(max_length=5000)
    proof2_type = models.CharField(max_length=200)
    proof3 = models.CharField(max_length=5000)
    proof3_type = models.CharField(max_length=200)
    proof4 = models.CharField(max_length=5000)
    proof4_type = models.CharField(max_length=200)
    category = models.CharField(max_length=2000)
    sub_category = models.CharField(max_length=2000)
    posted_from = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    feature_price = models.IntegerField(default=0)
    allowed_countries = models.CharField(max_length=50000)


class jobs_proofs(models.Model):
    proof1 = models.CharField(max_length=10000)
    proof2 = models.CharField(max_length=10000)
    proof3 = models.ImageField(upload_to="jobs proofs")
    proof4 = models.ImageField(upload_to="jobs proofs")
    job_id = models.CharField(max_length=4000)
    posted_by = models.CharField(max_length=3000)
    user_submitted_job = models.CharField(max_length=3000)
    title = models.CharField(max_length=3000)
    job_earning = models.FloatField()
    status = models.CharField(max_length=3000)


class notifications(models.Model):
    title = models.CharField(max_length=30000)
    url = models.CharField(max_length=2000)
    bell_digit = models.IntegerField()
    to_user = models.CharField(max_length=3000)
    date = models.CharField(max_length=3000)
    unseen = models.BooleanField()


class payment_history(models.Model):
    user = models.CharField(max_length=2000)
    payment_account = models.CharField(max_length=2000)
    payment_proof = models.ImageField(upload_to="Payment history")
    TID = models.CharField(max_length=2000)


class contacts(models.Model):
    email = models.EmailField()
    whatsapp = models.CharField(max_length=100)
    subject = models.CharField(max_length=1200)
    message = models.TextField()


class withdraw(models.Model):
    user = models.CharField(max_length=300)
    amount_to_withdraw = models.FloatField()
    payment_method = models.CharField(max_length=3000)
    payment_account_info = models.CharField(max_length=3000)
    status = models.BooleanField(default=False)
    paid_on = models.CharField(max_length=500)


class categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class subcategories(models.Model):
    name = models.CharField(max_length=200)
    belongs_to = models.ForeignKey("categories", on_delete=models.CASCADE)


class fake_proof_reports(models.Model):
    job_id = models.CharField(max_length=2000)
    proof_id = models.CharField(max_length=2000)
    job_owner = models.CharField(max_length=2200)
    user_submitted_job = models.CharField(max_length=2200)
    reason = models.TextField()


class chat_data(models.Model):
    user = models.CharField(max_length=200)
    message = models.TextField()
