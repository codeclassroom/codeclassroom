'''Jointly developed by Gagan Singh, Bhupesh Varshney & Animesh Ghosh.'''
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Institution(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Professor(models.Model):
    '''Assuming a professor can create multiple classrooms and each classroom can have 
    multiple assignments. if a classroom is deleted, all of the assignments of that class will
    delete automatically*.
    '''
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='ProfessorProfilePic', blank=True)
    institution = models.ForeignKey(to=Institution, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='StudentProfilePic', blank=True)
    institution = models.ForeignKey(to=Institution, blank=True, null=True, on_delete=models.CASCADE)
    course = models.CharField(max_length=50, blank=True)
    roll_no = models.IntegerField()

    def __str__(self):
        return self.user.username


class Classroom(models.Model):
    professor = models.ForeignKey(to=Professor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    students = models.ManyToManyField(to=Student, blank=True)
    '''because a student can join multiple classroom and each classroom can have multiple 
    students'''

    class Meta:
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return self.title


class Assignment(models.Model):
    classroom = models.ForeignKey(to=Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    deadline = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    assignment = models.ForeignKey(to=Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    marks = models.IntegerField()
    draft = models.BooleanField(default=False)

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
    status = models.CharField(max_length=100, choices=STATUS)
    submission = models.FileField(
        upload_to=f'assignments/{assignment}/questions/{question}/submissions/{student}',
        blank=False
    )
    remark = models.CharField(max_length=500, blank=True)
    # this field may be filled by prof as remark
