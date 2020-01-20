from django.core.mail import send_mail
from app.models import (
    Professor, Question, Assignment,
    Classroom, User
)

TO_EMAIL = 'varshneybhupesh@gmail.com'


def feedback(email, message):
    send_mail(
        'User FeedBack',
        message,
        email,
        [TO_EMAIL],
        fail_silently=False,
    )
    return True


def report(question, message):
    assignment = Question.objects.filter(pk=question).values('assignment')[0]
    classroom = Assignment.objects.filter(
        pk=assignment['assignment']).values('classroom')[0]
    professor = Classroom.objects.filter(
        pk=classroom['classroom']).values('professor')[0]
    user = Professor.objects.filter(
        pk=professor['professor']).values('user_id')[0]
    user_email = User.objects.get(pk=user["user_id"]).email

    question_title = Question.objects.get(pk=question).title
    print(question_title)

    full_message = """
    Question titled "{question_title}" has been reported by a user.
    FeedBack:
    {message}""".format(
        question_title=question_title,
        message=message
    )

    send_mail(
        'Reported Question',
        full_message,
        TO_EMAIL,
        [user_email],
        fail_silently=False,
    )

    return True
