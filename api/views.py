'''API views.'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import viewsets
from app.models import (Professor, Student,)
from app.serializers import (
    ProfessorSignupSerializer, ProfessorSerializer,
    StudentSignupSerializer, StudentSerializer,
)


@api_view(['GET'])
def index(request):
    '''API root.'''
    return Response(
        {
            'signup-professor': reverse('prof-signup', request=request),
            'signup-student': reverse('student-signup', request=request),
            'students': reverse('students', request=request),
            'professors': reverse('professors', request=request),
        }
    )


class ProfessorSignupView(generics.CreateAPIView):
    '''API view for signing-up professors.'''
    queryset = Professor.objects.all()
    serializer_class = ProfessorSignupSerializer


class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    '''API view for listing professors.'''
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class StudentSignupView(generics.CreateAPIView):
    '''API view for signing-up students.'''
    queryset = Student.objects.all()
    serializer_class = StudentSignupSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    '''API view for listing students.'''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
