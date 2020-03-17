from pprint import pprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from .models import Professor, Student, Classroom
from .forms import SignupForm, ClassroomCreateForm, ClassroomEditForm


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:dashboard'))

    return render(request, 'app/index.html')


def signup(request):
    context = { 'title' : 'Signup' }

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Signup Successful!')
            return redirect(reverse('app:login'))

        else:
            context['form'] = form
            return render(request, 'app/signup.html', context)

    elif request.method == 'GET':
        context['form'] = SignupForm(auto_id=True)
        return render(request, 'app/signup.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def dashboard(request):
    context = { 'title' : 'Dashboard' }

    user = request.user

    if user.is_authenticated:
        professor = Professor.objects.filter(user=user).first()
        student = Student.objects.filter(user=user).first()

        if professor is not None:
            context['professor'] = professor
            context['classrooms'] = Classroom.objects.filter(professor=professor)
            return render(request, 'app/dashboard-professor.html', context)

        elif student is not None:
            context['student'] = student
            context['classrooms'] = student.classroom_set.all()
            return render(request, 'app/dashboard-student.html', context)

        else:
            return redirect(reverse('app:login'))


@login_required(login_url=reverse_lazy('app:login'))
def create_classroom(request):
    context = { 'title' : 'Create Classroom' }
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    if request.method == 'GET':
        context['form'] = ClassroomCreateForm(
            professor=professor,
            auto_id=True,
        )
        return render(request, 'app/create-classroom.html', context)

    elif request.method == 'POST':
        form = ClassroomCreateForm(
            request.POST,
            professor=professor,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Classroom Created!')
            return redirect(reverse('app:dashboard'))

        else:
            context['form'] = form
            return render(request, 'app/create-classroom.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def classroom(request, pk):
    classroom = Classroom.objects.filter(pk=pk).first()

    if classroom is None:
        return HttpResponse('Not a valid classroom.')

    students = classroom.students.all()
    context = {
        'title' : 'Edit {classroom}'.format(classroom=classroom.title),
        'pk' : pk,
        'classroom' : classroom,
        'students' : students,
    }

    return render(request, 'app/classroom.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def edit_classroom(request, pk):
    classroom = Classroom.objects.filter(pk=pk).first()

    if classroom is None:
        return HttpResponse('Not a valid classroom.')

    context = { 'title' : 'Edit {classroom}'.format(classroom=classroom.title), }
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Request not allowed.')

    if request.method == 'GET':
        print(professor.institution)

        context['pk'] = pk
        context['form'] = ClassroomEditForm(
            instance=classroom,
            professor=professor,
            auto_id=True,
        )

        return render(request, 'app/edit-classroom.html', context)

    elif request.method == 'POST':
        form = ClassroomEditForm(
            request.POST,
            instance=classroom,
            professor=professor,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Classroom updated!')
            return redirect(reverse('app:dashboard'))

        else:
            context['form'] = form
            return render(request, 'app/edit-classroom.html', context)


def docs(request):
	return render(request, 'docs.html')
