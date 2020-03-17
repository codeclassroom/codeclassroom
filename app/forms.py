from pprint import pprint
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Professor, Student, Classroom


class SignupForm(UserCreationForm):
    PROFESSOR = 'professor'
    STUDENT = 'student'

    USER_TYPE_CHOICE = (
        (PROFESSOR, 'Professor',),
        (STUDENT, 'Student',),
    )

    user_type = forms.ChoiceField(required=True, choices=USER_TYPE_CHOICE, widget=forms.RadioSelect)

    def save(self, commit=True):
        # save user and get the type of user
        user = super().save()
        user_type = self.cleaned_data.get('user_type')

        # save either as professor or student and return the instance
        if user_type == 'professor':
            professor = Professor.objects.create(user=user)

            if commit:
                professor.save()

            return professor

        elif user_type == 'student':
            student = Student.objects.create(user=user)

            if commit:
                student.save()

            return student

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + (
            'email',
            'user_type',
        )


class ClassroomCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.professor = kwargs.pop('professor')
        institution = self.professor.institution

        super().__init__(*args, **kwargs)

        self.fields['professor'] = forms.ModelChoiceField(
            queryset=Professor.objects.filter(
                institution=institution,
            ),
            initial=self.professor,
            widget=forms.HiddenInput,
        )
        self.fields['students'] = forms.ModelMultipleChoiceField(
            queryset=Student.objects.filter(
                institution=institution,
            ),
            required=False,
        )

    def save(self, commit=True):
        classroom = super().save(commit=False)
        classroom.professor = self.professor

        if commit:
            classroom.save()
            classroom.students.set(self.cleaned_data['students'])

        return classroom

    class Meta:
        model = Classroom
        fields = (
            'title',
        )


class ClassroomEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.professor = kwargs.pop('professor')
        self.classroom = kwargs['instance']
        institution = self.professor.institution
        students = self.classroom.students.all()

        super().__init__(*args, **kwargs)

        self.fields['students'] = forms.ModelMultipleChoiceField(
            queryset=Student.objects.filter(
                institution=institution,
            ),
            initial=students,
            required=False,
        )

    def save(self):
        self.classroom.title = self.cleaned_data['title']
        self.classroom.students.set(self.cleaned_data['students'])

        self.classroom.save()

    class Meta:
        model = Classroom
        fields = (
            'title',
        )
