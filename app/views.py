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
    SignupForm, ClassroomCreateForm, ClassroomJoinForm, ClassroomEditForm,
    AssignmentCreateForm, AssignmentEditForm, QuestionCreateForm,
    QuestionEditForm,
)


def index(request):
    if request.user.is_authenticated:
        return redirect('app:classrooms')

    return render(request, 'app/cc-index.html')


def about(request):
    return render(request, 'app/about.html')


def faq(request):
    return render(request, 'app/faq.html')


def signup(request):
    context = {'title': 'Signup'}

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


@login_required
def dashboard(request):
    '''View that will be shown once a user logs in.'''
    context = {'title': 'Dashboard'}

    user = request.user

    professor = Professor.objects.filter(user=user).first()
    student = Student.objects.filter(user=user).first()

    if professor is not None:
        context['professor'] = professor
        context['classrooms'] = Classroom.objects.filter(
            professor=professor)

    elif student is not None:
        context['student'] = student
        context['classrooms'] = student.classroom_set.all()

    return render(request, 'app/cc-dashboard.html', context)


@login_required
def classrooms(request):
    '''
    View to list out classrooms and also handle classroom creation.

    Default view users will redirect to after logging in.
    '''
    context = {'title': 'Classrooms'}
    user = request.user

    if request.method == 'GET':
        professor = Professor.objects.filter(user=user).first()
        student = Student.objects.filter(user=user).first()

        if professor is not None:
            context['professor'] = professor
            context['classrooms'] = Classroom.objects.filter(
                professor=professor)
            context['form'] = ClassroomCreateForm(professor=professor, auto_id=True)

        elif student is not None:
            context['student'] = student
            context['classrooms'] = student.classroom_set.all()

    elif request.method == 'POST':
        professor = Professor.objects.filter(user=user).first()

        if professor is None:
            return HttpResponse('Not a professor!')

        form = ClassroomCreateForm(request.POST, professor=professor, auto_id=True)

        if form.is_valid():
            form.save()

            messages.success(request, 'Classroom Created!')

            return redirect('app:classrooms')

        else:
            context['form'] = form

    return render(request, 'app/cc-classrooms.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def create_classroom(request):
    context = {'title': 'Create Classroom'}
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
def join_classroom(request):
    student = Student.objects.filter(user=request.user).first()

    if student is None:
        return HttpResponse('Not allowed.')

    context = {
        'title': 'Join a Classroom',
    }

    if request.method == 'GET':
        context['form'] = ClassroomJoinForm(
            auto_id=True,
        )

        return render(request, 'app/join-classroom.html', context)

    elif request.method == 'POST':
        form = ClassroomJoinForm(
            request.POST,
            auto_id=True,
        )

        if form.is_valid():
            join_code = form.cleaned_data['join_code']

            classroom = Classroom.objects.filter(join_code=join_code).first()

            if classroom is None:
                context['form'] = form
                messages.error(request, 'No classrooms with given join code.')
                return render(request, 'app/join-classroom.html', context)

            else:
                if student in classroom.students.all():

                    messages.warning(request, 'Already in Classroom!')
                    return redirect(reverse('app:dashboard'))

                else:
                    classroom.students.add(student)
                    messages.success(request, 'Joined classroom!')

                return redirect(reverse('app:dashboard'))

        else:
            context['form'] = form

            return render(request, 'app/join-classroom', context)


# TODO: add edit classroom functionality to this view
@login_required
def classroom(request, pk):
    '''View to show classroom info such as the students, assignments etc.'''
    classroom = Classroom.objects.filter(pk=pk).first()

    if classroom is None:
        return HttpResponse('Not a valid classroom.')

    professor = Professor.objects.filter(user=request.user).first()
    student = Student.objects.filter(user=request.user).first()

    students = classroom.students.all()
    assignments = classroom.assignment_set.all()
    context = {
        'title': classroom.title,
        'pk': pk,
        'classroom': classroom,
        'students': students,
        'assignments': assignments,
    }

    if professor is not None:
        context['professor'] = professor

    elif student is not None:
        context['student'] = student

    return render(request, 'app/cc-classroom.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def edit_classroom(request, pk):
    classroom = Classroom.objects.filter(pk=pk).first()

    if classroom is None:
        return HttpResponse('Not a valid classroom.')

    context = {'title': 'Edit {classroom}'.format(classroom=classroom.title), }
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


# TODO: add create assignment functionality to view
@login_required
def assignments(request):
    '''View to list out assignments and also handle assignment creation.'''
    context = {'title': 'Assignments'}

    if request.method == 'GET':
        professor = Professor.objects.filter(user=request.user).first()
        student = Student.objects.filter(user=request.user)
        # .first()

        if professor is not None:
            context['professor'] = professor
            classrooms = Classroom.objects.filter(professor=professor)

        elif student is not None:
            context['student'] = student
            classrooms = Classroom.objects.filter(students__in=student)

        print(classrooms)

        assignments_list = []

        for classroom in classrooms:
            for assignment in classroom.assignment_set.all():
                assignments_list.append(assignment)

        print(assignments_list)

        context['assignments'] = assignments_list

    return render(request, 'app/cc-assignments.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def create_assignment(request):
    context = {'title': 'Create Assignment'}
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(professor=professor).first()

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
                'pk': classroom.id,
            }))

        else:
            context['form'] = form
            return render(request, 'app/create-assignment.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def assignment(request, pk):
    '''View to show info about assignment and list out the questions.'''
    professor = Professor.objects.filter(user=request.user).first()
    student = Student.objects.filter(user=request.user).first()

    if professor is not None:
        class_room = Classroom.objects.filter(professor=professor).first()

    elif student is not None:
        class_room = Classroom.objects.filter(students__user__username=student).first()

    assignment = Assignment.objects.filter(classroom=class_room).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    if professor:
        questions = assignment.question_set.all()

    if student:
        questions = assignment.question_set.filter(draft=False)

    context = {
        'title': '{classroom} - {assignment}'.format(
            classroom=class_room,
            assignment=assignment,
        ),
        'assignment': assignment,
        'classroom': class_room,
        'questions': questions
    }

    if professor is not None:
        context['professor'] = professor

    elif student is not None:
        context['student'] = student

    return render(request, 'app/assignment.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def edit_assignment(request, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(professor=professor).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    context = {
        'title': 'Edit {assignment} of {classroom}'.format(
            assignment=assignment,
            classroom=classroom,
        ),
        'assignment': assignment,
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
                'pk': assignment.id,
            }))

        else:
            context['form'] = form
            return render(request, 'app/edit-assignment.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def create_question(request, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    classroom = Classroom.objects.filter(professor=professor).first()

    if classroom is None:
        return HttpResponse('No valid classroom.')

    assignment = Assignment.objects.filter(pk=pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    context = {
        'title': '{classroom} - {assignment} - Add question'.format(
            classroom=classroom,
            assignment=assignment,
        ),
        'assignment_pk': assignment.id,
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
                'pk': assignment.id
            }))

        else:
            context['form'] = form
            return render(request, 'app/create-question.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def question(request, assignment_pk, pk):
    professor = Professor.objects.filter(user=request.user).first()
    student = Student.objects.filter(user=request.user).first()

    assignment = Assignment.objects.filter(pk=assignment_pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    question = Question.objects.filter(pk=pk).first()

    if question is None:
        return HttpResponse('No valid question.')

    context = {
        'title': '{question} - {assignment}'.format(
            assignment=assignment,
            question=question.title,
        ),
        'assignment_pk': assignment_pk,
        'question': question,
        'assignment': assignment,
        'student': student
    }

    if professor is not None:
        context['professor'] = professor

    elif student is not None:
        context['student'] = student

    return render(request, 'app/question.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def edit_question(request, assignment_pk, pk):
    professor = Professor.objects.filter(user=request.user).first()

    if professor is None:
        return HttpResponse('Not allowed.')

    assignment = Assignment.objects.filter(pk=assignment_pk).first()

    if assignment is None:
        return HttpResponse('No valid assignment.')

    question = Question.objects.filter(pk=pk).first()

    if question is None:
        return HttpResponse('No valid question.')

    context = {
        'title': 'Edit Question',
        #'classroom_pk': classroom_pk,
        'assignment_pk': assignment_pk,
        'pk': question.id,
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
                'assignment_pk': assignment_pk,
                'pk': question.id,
            }))

        else:
            context['form'] = form

            return render(request, 'app/edit-question.html', context)


def docs(request):
    return render(request, 'docs.html')


@login_required(login_url=reverse_lazy('app:login'))
def all_classrooms(request):
    '''View all classrooms of a current logged in user'''

    professor = Professor.objects.filter(user=request.user).first()
    student = Student.objects.filter(user=request.user).first()

    if professor is not None:
        query_class = Classroom.objects.filter(professor=professor)
        context = {
            'classrooms': query_class
        }

    elif student is not None:
        query_class = Classroom.objects.filter(students__user__username=student)
        context = {
            'classrooms': query_class
        }

    return render(request, 'app/classroom.html', context)


@login_required(login_url=reverse_lazy('app:login'))
def all_assignments(request):
    '''View all assignments of a current logged in user'''

    professor = Professor.objects.filter(user=request.user).first()
    student = Student.objects.filter(user=request.user).first()

    if professor is not None:
        class_room = Classroom.objects.filter(professor=professor).first()
        assignments = Assignment.objects.filter(classroom=class_room)
        context = {
            'title': 'Assignments',
            'assignments': assignments,
            'professor': professor
        }

    elif student is not None:
        class_room = Classroom.objects.filter(students__user__username=student).first()
        assignments = Assignment.objects.filter(classroom=class_room)
        context = {
            'title': 'Assignments',
            'assignments': assignments
        }

    return render(request, 'app/assignment.html', context)
