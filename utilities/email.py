from smtplib import SMTPException

from django.core.mail import send_mail

from app.models import Assignment, Classroom, Professor, Question, User

FROM_EMAIL = 'codeclassroom.contact@gmail.com'


def feedback(data: dict):
    try:
        if "email" in data:
            send_mail(
                'User Feedback',
                data["message"],
                data["email"],
                [FROM_EMAIL],
                fail_silently=False,
            )
        else:
            send_mail(
                'User Feedback',
                data["message"],
                "Anonymous User",
                [FROM_EMAIL],
                fail_silently=False,
            )
        return True
    except SMTPException:
        return False


def report(data: dict):
    question = data["question"]
    message = data["message"]
    assignment = Question.objects.filter(pk=question).values('assignment')[0]
    question_title = Question.objects.get(pk=question).title
    classroom = Assignment.objects.filter(
        pk=assignment['assignment']).values('classroom')[0]
    professor = Classroom.objects.filter(
        pk=classroom['classroom']).values('professor')[0]
    user = Professor.objects.filter(
        pk=professor['professor']).values('user_id')[0]
    professor_email = User.objects.get(pk=user["user_id"]).email

    if "email" in data:
        full_message = """
        Question titled "{question_title}" has been reported by a user.
        User {email} provided following Feedback on this question:
        {message}""".format(
            question_title=question_title,
            email=data["email"],
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
            FROM_EMAIL,
            [professor_email],
            fail_silently=False,
        )
        return True
    except SMTPException:
        return False


def plagiarism_report(data: dict):
    """Accepts User id instead of Student ID"""
    students = User.objects.filter(
        pk__in=[data["student_1"], data["student_2"]])
    student_emails = [student.email for student in students]

    try:
        send_mail(
            'You submission was suspected for plagiarism',
            data["template"],
            FROM_EMAIL,
            student_emails,
            fail_silently=False,
        )
        return True
    except SMTPException:
        return False
