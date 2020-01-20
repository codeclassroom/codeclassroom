from django.core.mail import send_mail
from app.models import (
    Professor, Question, Assignment,
    Classroom, User
)

TO_EMAIL = 'varshneybhupesh@gmail.com'


def feedback(email, message):
    try:
        send_mail(
            'User Feedback',
            message,
            email,
            [TO_EMAIL],
            fail_silently=False,
        )
        return True
    except smtplib.SMTPException:
        return False


def report(question, message, email):
    assignment = Question.objects.filter(pk=question).values('assignment')[0]
    classroom = Assignment.objects.filter(
        pk=assignment['assignment']).values('classroom')[0]
    professor = Classroom.objects.filter(
        pk=classroom['classroom']).values('professor')[0]
    user = Professor.objects.filter(
        pk=professor['professor']).values('user_id')[0]
    professor_email = User.objects.get(pk=user["user_id"]).email

    question_title = Question.objects.get(pk=question).title

    if email != "":
        full_message = """
        Question titled "{question_title}" has been reported by a user.
        User {email} provided following Feedback on this question:
        {message}""".format(
            question_title=question_title,
            email=email,
            message=message
        )
    else:
        full_message = """
        Question titled "{question_title}" has been reported by a user.
        Feedback:
        {message}""".format(
            question_title=question_title,
            message=message
        )

    try:
        send_mail(
            'Question Feedback',
            full_message,
            TO_EMAIL,
            [professor_email],
            fail_silently=False,
        )
        return True
    except smtplib.SMTPException:
        return False


