from pprint import pprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from .models import (
    Professor, Student, Classroom, Assignment, Question
)
from .forms import (
    SignupForm, ClassroomCreateForm, ClassroomEditForm,
    AssignmentCreateForm, AssignmentEditForm, QuestionCreateForm,
    QuestionEditForm,
)


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
    '''View that will be shown once a user logs in.'''
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
    '''View that shows classroom info such as the students, assignments etc.'''
    classroom = Classroom.objects.filter(pk=pk).first()

    if classroom is None:
        return HttpResponse('Not a valid classroom.')

    students = classroom.students.all()
    assignments = classroom.assignment_set.all()
    context = {
        'title' : classroom.title,
        'pk' : pk,
        'classroom' : classroom,
        'students' : students,
        'assignments' : assignments,
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


@login_required(login_url=reverse_lazy('app:login'))
def create_assignment(request, classroom_pk):
    context = { 'title' : 'Create Assignment' , 'classroom_pk' : classroom_pk }
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(pk=classroom_pk).first()

    if classroom is None:
        return HttpResponse('Invalid classroom.')

    if request.method == 'GET':
        context['form'] = AssignmentCreateForm(
            classroom=classroom,
            auto_id=True,
        )
        return render(request, 'app/create-assignment.html', context)

    elif request.method == 'POST':
        form = AssignmentCreateForm(
            request.POST,
            classroom=classroom,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Assignment Created!')
            return redirect(reverse('app:view-classroom', kwargs={
                'pk' : classroom.id,
            }))

        else:
            context['form'] = form
            return render(request, 'app/create-assignment.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def assignment(request, classroom_pk, pk):
    '''View to show info about assignment and list out the questions.'''
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(pk=classroom_pk).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    questions = assignment.question_set.all()

    context = {
        'title' : '{classroom} - {assignment}'.format(
            classroom=classroom,
            assignment=assignment,
        ),
        'classroom_pk' : classroom_pk,
        'assignment' : assignment,
        'questions' : questions,
    }

    return render(request, 'app/assignment.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def edit_assignment(request, classroom_pk, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(pk=classroom_pk).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    context = {
        'title' : 'Edit {assignment} of {classroom}'.format(
            assignment=assignment,
            classroom=classroom,
        ),
        'assignment' : assignment,
    }
    if request.method == 'GET':
        context['form'] = AssignmentEditForm(
            instance=assignment,
            auto_id=True,
        )
        return render(request, 'app/edit-assignment.html', context)

    elif request.method == 'POST':
        form = AssignmentEditForm(
            request.POST,
            instance=assignment,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Assignment Updated!')
            return redirect(reverse('app:view-assignment', kwargs={
                'classroom_pk' : classroom_pk,
                'pk' : assignment.id,
            }))

        else:
            context['form'] = form
            return render(request, 'app/edit-assignment.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def create_question(request, classroom_pk, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(pk=classroom_pk).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    context = {
        'title' : '{classroom} - {assignment} - Add question'.format(
            classroom=classroom,
            assignment=assignment,
        ),
        'classroom_pk' : classroom_pk,
        'assignment_pk' : assignment.id,
    }

    if request.method == 'GET':
        context['form'] = QuestionCreateForm(
            assignment=assignment,
            auto_id=True,
        )

        return render(request, 'app/create-question.html', context)

    elif request.method == 'POST':
        form = QuestionCreateForm(
            request.POST,
            assignment=assignment,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Question added!')
            return redirect(reverse('app:view-assignment', kwargs={
                'classroom_pk' : classroom_pk,
                'pk' : assignment.id
            }))

        else:
            context['form'] = form
            return render(request, 'app/create-question.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def question(request, classroom_pk, assignment_pk, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(pk=classroom_pk).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=assignment_pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    question = Question.objects.filter(pk=pk).first()

    if question is None:
        return HttpResponse('No valid question.')

    context = {
        'title' : '{classroom} - {assignment} - {question}'.format(
            classroom=classroom,
            assignment=assignment,
            question=question.title,
        ),
        'classroom_pk' : classroom_pk,
        'assignment_pk' : assignment_pk,
        'question' : question,
    }

    return render(request, 'app/question.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def edit_question(request, classroom_pk, assignment_pk, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(pk=classroom_pk).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=assignment_pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    question = Question.objects.filter(pk=pk).first()

    if question is None:
        return HttpResponse('No valid question.')

    context = {
        'title' : 'Edit Question - {question} - {assignment} - {classroom}'.format(
            classroom=classroom,
            assignment=assignment,
            question=question.title,
        ),
        'classroom_pk' : classroom_pk,
        'assignment_pk' : assignment_pk,
        'pk' : question.id,
    }
    if request.method == 'GET':
        context['form'] = QuestionEditForm(
            instance=question,
            auto_id=True,
        )

        return render(request, 'app/edit-question.html', context)

    elif request.method == 'POST':
        form = QuestionEditForm(
            request.POST,
            instance=question,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Question Updated!')
            return redirect(reverse('app:view-question', kwargs={
                'classroom_pk' : classroom_pk,
                'assignment_pk' : assignment_pk,
                'pk' : question.id,
            }))

        else:
            context['form'] = form

            return render(request, 'app/edit-question.html', context)

def docs(request):
	return render(request, 'docs.html')
