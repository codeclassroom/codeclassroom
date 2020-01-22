from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (AssignmentCreate, AssignmentDetail, AssignmentList,
                    ClassroomCreateView, ClassroomDetail, ClassroomJoinView,
                    ClassroomList, FeedBackView, JudgeCode, PlagiarismReport,
                    PlagiarismView, ProfessorDetail, ProfessorSignupView,
                    ProfessorViewSet, QuestionCreate, QuestionDetail,
                    QuestionList, ReportQuesiton, StudentDetail,
                    StudentSignupView, StudentViewSet, SubmissionCreate,
                    SubmissionDetail, SubmissionList, UserLoginView,
                    UserLogoutView)

schema_view = get_schema_view(
   openapi.Info(
      title="CodeClassroom API",
      default_version='v2.1.0',
      description="A platform for managing programming assignments in colleges & universities.",
      contact=openapi.Contact(email="varshneybhupes@gmail.com"),
      license=openapi.License(name="AGPL-3.0"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


student_list = StudentViewSet.as_view({'get': 'list'})
student_detail = StudentViewSet.as_view({'get': 'retrieve'})

professor_list = ProfessorViewSet.as_view({'get': 'list'})
professor_detail = ProfessorViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('signup/professor', ProfessorSignupView.as_view(), name='prof-signup'),
    path('signup/student', StudentSignupView.as_view(), name='student-signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('students/', student_list, name='students'),
    path('students/<int:pk>', StudentDetail.as_view(), name='student'),
    path('professors/', professor_list, name='professors'),
    path('professors/<int:pk>', ProfessorDetail.as_view(), name='professor'),

    # All Classroom URLs
    path('classrooms/create', ClassroomCreateView.as_view(), name='classroom-create'),
    path('classrooms/join', ClassroomJoinView.as_view(), name='classroom-join'),
    path('classrooms/<int:pk>', ClassroomDetail.as_view(), name='classroom-detail'),
    path('classrooms', ClassroomList.as_view(), name='classrooms'),

    # All Assignment URLs
    path('assignments/create', AssignmentCreate.as_view(),
         name='assignment-create'),
    path('assignments', AssignmentList.as_view(), name='assignment-list'),
    path('assignments/<int:pk>', AssignmentDetail.as_view(), name='assignment-list'),

    # All Question URLs
    path('questions/create', QuestionCreate.as_view(), name='question-create'),
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),

    # All Solution/Submission URLs
    path('submissions/create', SubmissionCreate.as_view(), name='submission-create'),
    path('submissions/<int:pk>', SubmissionDetail.as_view(), name='submissions-detail'),
    path('submissions', SubmissionList.as_view(), name='submissions'),

    # Utility URLs
    path('judge/', JudgeCode.as_view(), name='code-judge'),
    path('codesim/', PlagiarismView.as_view(),
         name='plagiarism-detector'),
    path('email/feedback', FeedBackView.as_view(), name='feedback'),
    path('email/report', ReportQuesiton.as_view(), name='report-question'),
    path('email/plagiarism-report', PlagiarismReport.as_view(), name='report-plagiarism')

]
