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
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from app.models import (Professor, Student, Classroom, Assignment, Question, Solution)
from app.serializers import (
    UserLoginSerializer,
    ProfessorSignupSerializer, ProfessorSerializer,
    StudentSignupSerializer, StudentSerializer,
    ClassroomCreateSerializer, ClassroomJoincodeSerializer, ClassroomSerializer,
    AssignmentSerializer,
    QuestionSerializer,
    SolutionSerializer,
)
from utilities.judge import run_code, submit_code


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
        'create-classroom': reverse('classroom-create', request=request),
        'join-classroom': reverse('classroom-join', request=request),
        'classrooms': reverse('classrooms', request=request),
        'create-assignment': reverse('assignment-create', request=request),
        'create-question': reverse('question-create', request=request),
        'run-code': reverse('run-code', request=request),
        'submit-solution': reverse('submission-create', request=request),
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
                return Response(content, status=status.HTTP_202_ACCEPTED)

            else:
                content = {
                    'detail': "User either doesn't exist or has invalid credentials.",
                    'authenticated': False
                }
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(views.APIView):
    '''API view to logout an authenticated user.'''
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'logout': True}, status=status.HTTP_202_ACCEPTED)


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


class ClassroomCreateView(views.APIView):
    '''API view for creating a classroom.'''
    serializer_class = ClassroomCreateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClassroomCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomJoinView(views.APIView):
    '''API view for joining a classroom.'''
    # queryset = Classroom.objects.all()
    serializer_class = ClassroomJoincodeSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClassroomJoincodeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            join_code = serializer.data['join_code']
            student = Student.objects.get(user=request.user)

            classroom = Classroom.objects.get(join_code=join_code)
            classroom.students.add(student)
            return Response({'status': 'Student joined classroom.'}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomViewSet(viewsets.ReadOnlyModelViewSet):
    '''API view for listing classrooms.'''
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class AssignmentView(views.APIView):
    '''API view for listing assignments.'''
    serializer_class = AssignmentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):
        context = Assignment.objects.filter(classroom__id=class_id)
        serializer = AssignmentSerializer(context, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssignmentCreateView(views.APIView):
    '''API view for creating assignments.'''
    serializer_class = AssignmentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionView(views.APIView):
    '''API view for listing questions.'''
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, assg_id):
        context = Question.objects.filter(assignment__id=assg_id)
        serializer = QuestionSerializer(context, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionCreateView(views.APIView):
    '''API view for creating questions.'''
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RunCode(views.APIView):
    '''API for running code.'''
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data["code"]
        lang = request.data["language"]
        question = request.data["question_id"]

        content = run_code(code, lang, question)

        return Response(content, status=status.HTTP_200_OK)


class SolutionView(views.APIView):
    '''API view for submitting solutions.'''
    serializer_class = SolutionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = SolutionSerializer(data=request.data)
        print(request.data)

        if serializer.is_valid(raise_exception=True):
            question = request.data['question']
            assignment = request.data['assignment']

            file_obj = request.FILES['submission']
            code = str(file_obj.read().decode())

            context, execution_status = submit_code(question, assignment, code)

            serializer.save(status=execution_status)

            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSubmission(views.APIView):
    '''API View for returning submissions by a student.'''
    serializer_class = SolutionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, question, student):
        context = Solution.objects.filter(student_id=student, question_id=question).distinct()
        serializer = SolutionSerializer(context, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
