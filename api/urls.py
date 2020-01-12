from django.urls import path, include
from .views import (
    index,
    UserLoginView, UserLogoutView,
    StudentSignupView, StudentViewSet,
    ProfessorSignupView, ProfessorViewSet,
    ClassroomCreateView, ClassroomJoinView, ClassroomViewSet,
    AssignmentList, AssignmentCreate, AssignmentDetail,
    QuestionList, QuestionCreate, QuestionDetail,
    SubmissionCreate, SubmissionList, SubmissionDetail,
    PlagiarismView, RunCode
)


student_list = StudentViewSet.as_view({'get': 'list'})
student_detail = StudentViewSet.as_view({'get': 'retrieve'})

professor_list = ProfessorViewSet.as_view({'get': 'list'})
professor_detail = ProfessorViewSet.as_view({'get': 'retrieve'})

classroom_list = ClassroomViewSet.as_view({'get': 'list'})
classroom_detail = ClassroomViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('', index, name='index'),
    path('signup/professor', ProfessorSignupView.as_view(), name='prof-signup'),
    path('signup/student', StudentSignupView.as_view(), name='student-signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('students/', student_list, name='students'),
    path('students/<int:pk>/', student_detail, name='student'),
    path('professors/', professor_list, name='professors'),
    path('professors/<int:pk>/', professor_detail, name='student'),

    # All Classroom URLs
    path('classroom/create', ClassroomCreateView.as_view(), name='classroom-create'),
    path('classroom/join/', ClassroomJoinView.as_view(), name='classroom-join'),
    path('classroom/<int:pk>/', classroom_detail, name='classroom'),
    path('classrooms/', classroom_list, name='classrooms'),

    # All Assignment URLs
    path('assignment/create', AssignmentCreate.as_view(),
         name='assignment-create'),
    path('assignments', AssignmentList.as_view(), name='assignment-list'),
    path('assignments/<int:pk>', AssignmentDetail.as_view(), name='assignment-list'),

    # All Question URLs
    path('question/create', QuestionCreate.as_view(), name='question-create'),
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),

    # All Solution/Submission URLs
    path('submission/create', SubmissionCreate.as_view(), name='submission-create'),
    path('submissions/<int:pk>', SubmissionDetail.as_view(), name='submissions-detail'),
    path('submissions/', SubmissionList.as_view(), name='submissions'),

    # Utility URLs
    path('coderunner/', RunCode.as_view(), name='run-code'),
    path('plagiarism-detector/', PlagiarismView.as_view(),
         name='plagiarism-detector')

]
