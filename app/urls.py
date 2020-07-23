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
        },
    ), name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view(
        template_name='app/logout.html',
        extra_context={
            'title': 'Logout'
        },
    )), name='logout'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

    # classroom views
    path('classrooms/', views.classrooms, name='classrooms'),
    path('classrooms/<int:pk>', views.classroom, name='classroom'),
    path('classrooms/<int:pk>/edit', views.edit_classroom, name='edit-classroom'),
    path('classrooms/<int:pk>/delete', views.delete_classroom, name='delete-classroom'),

    # assignment views
    path('assignments/', views.assignments, name='assignments'),
    path('assignment/<int:pk>', views.assignment, name='assignment'),
    path('assignment/<int:pk>/edit', views.edit_assignment, name='edit-assignment'),
    path('assignment/<int:pk>/delete', views.delete_assignment, name='delete-assignment'),

    # question views
    path('question/<int:pk>', views.question, name='question'),
    path('question/<int:pk>/edit', views.edit_question, name='edit-question'),
    path('question/<int:pk>/delete', views.delete_question, name='delete-question'),

    # old views
    path('dashboard/classroom/join/', views.join_classroom, name='join-classroom'),
    path('dashboard/classroom/<int:pk>/', views.classroom, name='view-classroom'),
    # path('dashboard/classroom/<int:pk>/edit/', views.edit_classroom, name='edit-classroom'),

    path('dashboard/assignments/', views.all_assignments, name='all-assignments'),
    path('dashboard/assignment/create/', views.create_assignment, name='create-assignment'),
    path('dashboard/assignment/<int:pk>/', views.assignment, name='view-assignment'),
    # path('dashboard/assignment/<int:pk>/edit/', views.edit_assignment, name='edit-assignment'),

    path('dashboard/assignment/<int:pk>/question/create/', views.create_question, name='create-question'),
    path('dashboard/assignment/<int:assignment_pk>/question/<int:pk>/', views.question, name='view-question'),
    # path('dashboard/assignment/<int:assignment_pk>/question/<int:pk>/edit/', views.edit_question, name='edit-question'),
]
