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
    path('classroom/create/', views.create_classroom, name='create-classroom'),
    path('classroom/<int:pk>/', views.classroom, name='view-classroom'),
    path('classroom/edit/<int:pk>/', views.edit_classroom, name='edit-classroom'),

]
