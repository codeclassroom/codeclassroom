from pprint import pprint
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Professor, Student


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
        user = super(SignupForm, self).save()
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
