from django.urls import path, include
from .views import (
	index,
    UserLoginView, UserLogoutView,
	StudentSignupView, StudentViewSet,
	ProfessorSignupView, ProfessorViewSet
)


student_list = StudentViewSet.as_view({'get': 'list'})
student_detail = StudentViewSet.as_view({'get': 'retrieve'})
professor_list = ProfessorViewSet.as_view({'get': 'list'})
professor_detail = ProfessorViewSet.as_view({'get': 'retrieve'})


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
]
