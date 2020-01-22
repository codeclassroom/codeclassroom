'''API views.'''
from django.contrib.auth import authenticate, login, logout
from drf_yasg.utils import swagger_serializer_method
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from app.models import (Assignment, Classroom, Professor, Question, Solution,
                        Student)
from app.serializers import (AssignmentSerializer, ClassroomCreateSerializer,
                             ClassroomJoincodeSerializer, ClassroomSerializer,
                             FeedBackEmailSerializer, JudgeSerializer,
                             PlagiarismReportSerializer, PlagiarismSerializer,
                             ProfessorSerializer, ProfessorSignupSerializer,
                             QuestionSerializer, ReportQuestionSerializer,
                             SolutionSerializer, StudentSerializer,
                             StudentSignupSerializer, UserLoginSerializer)
from utilities.codesim import codesim
from utilities.email import feedback, plagiarism_report, report
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
        'code-judge': reverse('code-judge', request=request),
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


class ProfessorDetail(generics.RetrieveUpdateDestroyAPIView):
    '''API view for updating professors'''
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class StudentSignupView(generics.CreateAPIView):
    '''API view for signing-up students.'''
    queryset = Student.objects.all()
    serializer_class = StudentSignupSerializer
    permission_classes = [AllowAny]


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    '''API view for listing all students'''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    '''API view for updating students'''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ClassroomCreateView(views.APIView):
    '''API view for creating a classroom'''
    serializer_class = ClassroomCreateSerializer

    @swagger_serializer_method(serializer_or_field=ClassroomCreateSerializer)
    def post(self, request):
        serializer = ClassroomCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomJoinView(generics.CreateAPIView):
    '''API view for joining a classroom'''
    serializer_class = ClassroomJoincodeSerializer

    @swagger_serializer_method(serializer_or_field=ClassroomJoincodeSerializer)
    def post(self, request):
        serializer = ClassroomJoincodeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            join_code = serializer.data['join_code']
            student = Student.objects.get(user=request.user)

            classroom = Classroom.objects.get(join_code=join_code)
            classroom.students.add(student)
            return Response({'status': 'Student joined classroom.'}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomList(generics.ListAPIView):
    '''API view for listing all sClassrooms'''
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()


class ClassroomDetail(generics.RetrieveUpdateDestroyAPIView):
    '''API view for updating Classroom'''
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()


class AssignmentCreate(generics.CreateAPIView):
    '''API view for creating assignments'''
    serializer_class = AssignmentSerializer

    @swagger_serializer_method(serializer_or_field=AssignmentSerializer)
    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentList(generics.ListAPIView):
    '''API view for all listing assignments'''
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()


class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    '''API View for updaating Assignment'''
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()


class QuestionCreate(generics.CreateAPIView):
    '''API view for creating questions'''
    serializer_class = QuestionSerializer

    @swagger_serializer_method(serializer_or_field=QuestionSerializer)
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionList(generics.ListAPIView):
    '''API view for listing all questions'''
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    '''API View for Updating Question'''
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class JudgeCode(generics.CreateAPIView):
    '''API for Judging Code'''
    serializer_class = JudgeSerializer

    @swagger_serializer_method(serializer_or_field=JudgeSerializer)
    def post(self, request):
        serializer = JudgeSerializer(data=request.data)
        if serializer.is_valid():
            code = request.data["code"]
            lang = request.data["language"]

            if request.data["testcases"] != "":
                content = run_code(code, lang, testcase=request.data["testcases"])
            elif request.data["question_id"] != "":
                question = request.data["question_id"]
                content = run_code(code, lang, question)

        return Response(content, status=status.HTTP_200_OK)


class SubmissionCreate(generics.CreateAPIView):
    '''API view for submitting solutions.'''
    serializer_class = SolutionSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_serializer_method(serializer_or_field=SolutionSerializer)
    def post(self, request):

        serializer = SolutionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            c = Classroom.objects.filter(students=request.data["student"])

            if c.exists():
                question = request.data['question']
                assignment = request.data['assignment']
                file_obj = request.FILES['submission']

                code = str(file_obj.read().decode())

                context, execution_status = submit_code(
                        question, assignment, code
                    )
                serializer.save(status=execution_status)
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"detail": "Student has not joined any classroom yet"},
                    status=status.HTTP_403_FORBIDDEN
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionList(generics.ListAPIView):
    '''API View for returning all submissions'''
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    '''API View for returning submissions by a student'''
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


class PlagiarismView(generics.CreateAPIView):
    '''API View for running Plagiarism Service'''
    serializer_class = PlagiarismSerializer

    @swagger_serializer_method(serializer_or_field=PlagiarismSerializer)
    def post(self, request):
        serializer = PlagiarismSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                Assignment.objects.get(pk=request.data["assignment"])
                results = codesim(request.data["assignment"])
                return Response(results, status=status.HTTP_200_OK)
            except Assignment.DoesNotExist:
                return Response(
                        {"detail": "Assignment Does Not Exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )


class FeedBackView(generics.CreateAPIView):
    """Anonymous Feedback for CodeClassroom Website Creators"""
    serializer_class = FeedBackEmailSerializer
    permission_classes = [AllowAny]

    @swagger_serializer_method(serializer_or_field=FeedBackEmailSerializer)
    def post(self, request):
        serializer = FeedBackEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email_status = feedback(serializer.data)
            if email_status:
                return Response(
                    {"detail": "Thanks for your feedback"},
                    status=status.HTTP_202_ACCEPTED
                    )
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportQuesiton(generics.CreateAPIView):
    """Report Professors for any error/feedback in Question by sending them an email"""
    serializer_class = ReportQuestionSerializer

    @swagger_serializer_method(serializer_or_field=ReportQuestionSerializer)
    def post(self, request):
        serializer = ReportQuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            report_status = report(serializer.data)
            if report_status:
                return Response(
                    {"detail": "Thanks for your feedback"},
                    status=status.HTTP_202_ACCEPTED
                    )
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlagiarismReport(generics.CreateAPIView):
    """Report Students for plagiarism by sending them an email
    Accepts User ID instead of Student ID"""
    serializer_class = PlagiarismReportSerializer

    @swagger_serializer_method(serializer_or_field=PlagiarismReportSerializer)
    def post(self, request):
        serializer = PlagiarismReportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            report_status = plagiarism_report(serializer.data)
            if report_status:
                return Response(
                    {"detail": "Students have been notified"},
                    status=status.HTTP_202_ACCEPTED
                    )
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
