'''Serializer classes for models using ModelSerializer. Serializing all fields.'''
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Institution, Student, Professor, Classroom, Assignment, Question, Solution
)


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = '__all__'


class UserSignupSerializer(serializers.ModelSerializer):
    '''Serializer for signing-up new users.'''
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for listing/retrieving existing users.'''

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfessorSignupSerializer(serializers.ModelSerializer):
    '''Serializer for signing-up new professors.'''
    user = UserSignupSerializer()

    class Meta:
        model = Professor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        professor = Professor.objects.create(user=user, **validated_data)
        return professor


class ProfessorSerializer(serializers.ModelSerializer):
    '''Serializer for listing/retrieving existing professors.'''
    user = UserSerializer()
    institution = serializers.StringRelatedField()

    class Meta:
        model = Professor
        fields = '__all__'


class StudentSignupSerializer(serializers.ModelSerializer):
    '''Serializer for signing-up new students.'''
    user = UserSignupSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class StudentSerializer(serializers.ModelSerializer):
    '''Serializer for listing/retrieving existing students.'''
    user = UserSerializer()
    institution = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'students'},
        }


class ClassroomCreateSerializer(serializers.ModelSerializer):
    join_code = serializers.CharField(read_only=True)

    class Meta:
        model = Classroom
        fields = ['professor', 'title', 'join_code']


class ClassroomJoincodeSerializer(serializers.Serializer):
    '''Serializer for the join code.'''
    join_code = serializers.CharField(max_length=5, min_length=5, allow_blank=False, required=True)


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = [
            'id', 'question', 'assignment', 'student',
            'sub_date', 'submission', 'remark'
        ]

    def create(self, validated_data):
        return Solution.objects.create(**validated_data)


class PlagiarismSerializer(serializers.Serializer):
    assignment = serializers.IntegerField()


class JudgeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    language = serializers.CharField(required=True)
    question = serializers.IntegerField(required=False)
    testcases = serializers.CharField(required=False)


class FeedBackEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    message = serializers.CharField(required=True)


class ReportQuestionSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    email = serializers.EmailField(required=False)
    message = serializers.CharField(required=True)


class PlagiarismReportSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    student_1 = serializers.IntegerField(required=True)
    student_2 = serializers.IntegerField(required=True)
    template = serializers.CharField(required=True)
