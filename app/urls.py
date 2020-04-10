from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path, reverse_lazy, include
from . import views

app_name = 'app'

question_pattterns = [
    path('create/', views.create_question, name='create-question'),
    path('<int:pk>/', views.question, name='view-question'),
    path('<int:pk>/edit/', views.edit_question, name='edit-question'),
]

assignment_patterns = [
    path('create/', views.create_assignment, name='create-assignment'),
    path('<int:pk>/', views.assignment, name='view-assignment'),
    path('<int:pk>/edit/', views.edit_assignment, name='edit-assignment'),
    path('<int:assignment_pk>/question/', include(question_pattterns)),
]

classroom_patterns = [
    path('create/', views.create_classroom, name='create-classroom'),
    path('join/', views.join_classroom, name='join-classroom'),
    path('<int:pk>/', views.classroom, name='view-classroom'),
    path('<int:pk>/edit/', views.edit_classroom, name='edit-classroom'),
    path('<int:classroom_pk>/assignment/', include(assignment_patterns)),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='app/login.html',
        extra_context={
            'title': 'Login',
            'form': AuthenticationForm(auto_id=True),
            'next': reverse_lazy('app:index'),
        },
    ), name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view(
        template_name='app/logout.html',
        extra_context={
            'title': 'Logout'
        }
    ), login_url=reverse_lazy('app:login')), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('classroom/', include(classroom_patterns)),
]
