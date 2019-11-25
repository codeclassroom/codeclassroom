from django.urls import path, include
from .views import (
	index,
    UserLoginView, UserLogoutView,
	StudentSignupView, StudentViewSet,
	ProfessorSignupView, ProfessorViewSet,
    ClassroomView, ClassroomViewSet,
    AssignmentView, AssignmentCreateView,
    QuestionView, QuestionCreateView,
    RunCode, SolutionView, GetSubmission
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
    
    path('classroom/create', ClassroomView.as_view(), name='classroom-create'),
    path('classroom/<int:pk>/', classroom_detail, name='classroom'),
    path('classrooms/', classroom_list, name='classrooms'),
    
    path('assignment/create', AssignmentCreateView.as_view(), name='assignment-create'),
    path('classroom/<int:class_id>/assignments', AssignmentView.as_view(), name='classroom-assignments'),

    path('question/create', QuestionCreateView.as_view(), name='question-create'),
    path('assignments/<int:assg_id>/questions/', QuestionView.as_view(), name='classroom-assignments-questions'),
    
    path('coderunner/', RunCode.as_view(), name='run-code'),
    path('submission/create', SolutionView.as_view(), name='submission-create'),
    path('submissions/<int:question>/<int:student>/', GetSubmission.as_view(), name='submissions'),

]
