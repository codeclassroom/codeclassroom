from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path, reverse_lazy
from . import views

app_name = 'app'
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
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/classrooms/', views.all_classrooms, name='all-classrooms'),
    path('dashboard/classroom/create/', views.create_classroom, name='create-classroom'),
    path('dashboard/classroom/join/', views.join_classroom, name='join-classroom'),
    path('dashboard/classroom/<int:pk>/', views.classroom, name='view-classroom'),
    path('dashboard/classroom/<int:pk>/edit/', views.edit_classroom, name='edit-classroom'),

    path('dashboard/assignments/', views.all_assignments, name='all-assignments'),
    path('dashboard/assignment/create/', views.create_assignment, name='create-assignment'),
    path('dashboard/assignment/<int:pk>/', views.assignment, name='view-assignment'),
    path('dashboard/assignment/<int:pk>/edit/', views.edit_assignment, name='edit-assignment'),

    path('dashboard/assignment/<int:pk>/question/create/', views.create_question, name='create-question'),
    path('dashboard/assignment/<int:assignment_pk>/question/<int:pk>/', views.question, name='view-question'),
    path('dashboard/assignment/<int:assignment_pk>/question/<int:pk>/edit/', views.edit_question, name='edit-question'),
]
