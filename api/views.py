'''API views.'''
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import viewsets
from app.models import (Professor, Student,)
from app.serializers import (
    UserLoginSerializer,
    ProfessorSignupSerializer, ProfessorSerializer,
    StudentSignupSerializer, StudentSerializer,
)


@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    '''API root.'''
    return Response({
        'signup-professor': reverse('prof-signup', request=request),
        'signup-student': reverse('student-signup', request=request),
        'login': reverse('login', request=request),
        'logout': reverse('logout', request=request),
        'students': reverse('students', request=request),
        'professors': reverse('professors', request=request),
    })


class UserLoginView(views.APIView):
    '''API view for logging-in users.'''
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.data['username']
            password = serializer.data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                content = {
                    'detail': 'User logged in.',
                    'authenticated': True
                }
                return Response(content)

            else:
                content = {
                    'detail': "User either doesn't exist or has invalid credentials.",
                    'authenticated': False
                }
                return Response(content)


class UserLogoutView(views.APIView):
    '''API view to logout an authenticated user.'''
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'logout': True})


class ProfessorSignupView(generics.CreateAPIView):
    '''API view for signing-up professors.'''
    queryset = Professor.objects.all()
    serializer_class = ProfessorSignupSerializer
    permission_classes = [AllowAny]


class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    '''API view for listing professors.'''
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class StudentSignupView(generics.CreateAPIView):
    '''API view for signing-up students.'''
    queryset = Student.objects.all()
    serializer_class = StudentSignupSerializer
    permission_classes = [AllowAny]


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    '''API view for listing students.'''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
