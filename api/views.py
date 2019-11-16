'''API views using mostly ModelViewSet.'''
from django.contrib.auth.models import User
from rest_framework import viewsets
from app.models import Student, Professor
from app.serializers import (
    UserSerializer, StudentSerializer, ProfessorSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    queryset = Professor.objects.all()
