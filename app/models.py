'''Jointly developed by Gagan Singh, Bhupesh Varshney & Animesh Ghosh.'''
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from app.storage import OverwriteStorage

def submission_directory_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/assignments/<assg_id>/questions/<ques_id/submissions/<student_id>
    """
    return 'assignments/{0}/questions/{1}/submissions/{2}/'.format(
        instance.assignment.id, instance.question.id, instance.student.id, filename)


def random_code(length=5):
    '''Returns a random code of given length'''
    code_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(population=code_chars, k=length))


class Institution(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Professor(models.Model):
    '''Assuming a professor can create multiple classrooms and each classroom can have 
    multiple assignments. if a classroom is deleted, all of the assignments of that class will
    delete automatically
    '''
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='ProfessorProfilePic', blank=True, null=True)
    institution = models.ForeignKey(to=Institution, blank=True, null=True, on_delete=models.CASCADE)
    moss_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='StudentProfilePic', blank=True, null=True)
    institution = models.ForeignKey(to=Institution, blank=True, null=True, on_delete=models.CASCADE)
    course = models.CharField(max_length=50, blank=True)
    roll_no = models.IntegerField()

    def __str__(self):
        return self.user.username


class Classroom(models.Model):
    professor = models.ForeignKey(to=Professor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    students = models.ManyToManyField(to=Student, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    # because a student can join multiple classrooms and each classroom can have multiple students
    join_code = models.CharField(max_length=5, default=random_code, editable=False, unique=True)

    class Meta:
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return self.title


class Assignment(models.Model):
    LANGUAGE = (
        ('Python3', 'Python3'),
        ('Java', 'Java'),
        ('C++', 'C++'),
        ('C', 'C'),
        ('PHP', 'PHP'),
        ('Bash', 'Bash')
    )
    classroom = models.ForeignKey(to=Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=50, choices=LANGUAGE)

    def __str__(self):
        return self.title


class Question(models.Model):
    assignment = models.ForeignKey(to=Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    marks = models.IntegerField(blank=True)
    draft = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Solution(models.Model):
    ACCEPTED = 'accepted'
    PARTIALLY_SUBMIT = 'partially-submit'
    WRONG = 'wrong'
    NOT_ATTEMPT = 'not-attempted'

    STATUS = (
        (ACCEPTED, 'Accepted'),
        (PARTIALLY_SUBMIT, 'Partially Submitted'),
        (WRONG, 'Wrong Answer'),
        (NOT_ATTEMPT, 'Not Attempted')
    )

    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    assignment = models.ForeignKey(to=Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    sub_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=STATUS, default=STATUS[3][0])
    submission = models.FileField(
        upload_to=submission_directory_path,
        blank=False,
        storage=OverwriteStorage()
    )
    remark = models.CharField(max_length=500, blank=True)
    # this field may be filled by prof as remark


class PlagResult(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    solution_1 = models.ForeignKey(to=Solution, on_delete=models.CASCADE, related_name='solution_1')
    solution_2 = models.ForeignKey(to=Solution, on_delete=models.CASCADE, related_name='solution_2')
    perc_1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    perc_2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    lines_matched = models.CharField(max_length=100)
    lines_match_count = models.IntegerField()
    moss_page_url = models.URLField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}-{}".format(self.solution_1, self.solution_2)
