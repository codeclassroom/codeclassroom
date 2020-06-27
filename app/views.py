'''
app's views to handle web-app requests.

Context variables to note:
title -- text that will go inside the title tag in this format: (CodeClassroom - {title})
active_link -- specifies which link in the sidebar shall be highlighted (see cc-base-dashboard.html)
add -- boolean which specifies whether or not "add button" will be shown or not
delete -- boolean which specifies whether or not delete button (made using an anchor tag) will work
'''

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
    NewAssignmentCreateForm, AssignmentCreateForm, AssignmentEditForm,
    QuestionCreateForm, QuestionEditForm,
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
def classrooms(request):
    '''
    View to list out classrooms and also handle classroom creation.

    Default view users will redirect to after logging in.
    '''
    context = {'title': 'Classrooms', 'active_link': 'classrooms'}
    user = request.user

    if request.method == 'GET':
        professor = Professor.objects.filter(user=user).first()
        student = Student.objects.filter(user=user).first()

        if professor:
            context['professor'] = professor
            context['classrooms'] = Classroom.objects.filter(
                professor=professor)
            context['form'] = ClassroomCreateForm(
                professor=professor, auto_id=True)
            context['add'] = True

        elif student:
            context['student'] = student
            context['classrooms'] = student.classroom_set.all()

    elif request.method == 'POST':
        professor = Professor.objects.filter(user=user).first()

        if not professor:
            return HttpResponse('Not a professor!')

        form = ClassroomCreateForm(
            request.POST, professor=professor, auto_id=True)

        if form.is_valid():
            form.save()

            messages.success(request, 'Classroom Created!')

            return redirect('app:classrooms')

        else:
            context['form'] = form

    return render(request, 'app/cc-classrooms.html', context)


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


# TODO: add edit, delete classroom functionality to this view
@login_required
def classroom(request, pk):
    '''
    View to show classroom info such as the students, assignments etc.

    Also handles assignment creation (easy to get related classroom from pk).
    '''
    classroom = Classroom.objects.filter(pk=pk).first()

    if not classroom:
        return HttpResponse('Not a valid classroom.')

    if request.method == 'GET':
        professor = Professor.objects.filter(user=request.user).first()
        student = Student.objects.filter(user=request.user).first()

        students = classroom.students.all()
        assignments = classroom.assignment_set.all()
        context = {
            'title': classroom.title,
            'active_link': 'classrooms',
            'classroom': classroom,
            'students': students,
            'assignments': assignments,
        }

        if professor:
            context['professor'] = professor
            context['form'] = AssignmentCreateForm(
                classroom=classroom, auto_id=True)
            context['add'] = True
            context['delete'] = True

        elif student:
            context['student'] = student

    # creating assignment for related classroom
    elif request.method == 'POST':
        form = AssignmentCreateForm(
            request.POST,
            classroom=classroom,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Assignment Created!')
            return redirect('app:classroom', pk=classroom.pk)

        else:
            context['form'] = form

    return render(request, 'app/cc-classroom.html', context)


@login_required
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
            return redirect('app:classroom', pk=pk)

        else:
            context['form'] = form
            return render(request, 'app/edit-classroom.html', context)


@login_required
def delete_classroom(request, pk):
    '''View to delete classroom.'''

    classroom = Classroom.objects.filter(pk=pk).first()
    classroom.delete()

    messages.success(request, 'Classroom deleted!')

    return redirect('app:classrooms')


@login_required
def assignments(request):
    '''View to list out assignments ~~and also handle assignment creation~~.'''
    context = {'title': 'Assignments', 'active_link': 'assignments'}

    if request.method == 'GET':
        professor = Professor.objects.filter(user=request.user).first()
        student = Student.objects.filter(user=request.user)

        if professor:
            context['professor'] = professor
            assignments_list = Assignment.objects.filter(
                classroom__professor=professor)
            context['delete'] = True

        elif student:
            context['student'] = student
            assignments_list = Assignment.objects.filter(
                classroom__students__in=student)

        context['assignments'] = assignments_list
        context['form'] = NewAssignmentCreateForm(auto_id=True)

        return render(request, 'app/cc-assignments.html', context)

    # POST request from cc-classroom.html
    # this will now not run
    elif request.method == 'POST':
        form = AssignmentCreateForm(
            request.POST,
            classroom=classroom,
            auto_id=True,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Assignment Created!')
            return redirect(reverse('app:classroom', kwargs={
                'pk': classroom.id,
            }))

        else:
            context['form'] = form
            return render(request, 'app/cc-classroom.html', context)


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


@login_required
def assignment(request, pk):
    '''
    View to show info about assignment and list out the questions.

    Also handles question creation.
    '''
    assignment = Assignment.objects.filter(pk=pk).first()

    if not assignment:
        return HttpResponse('No valid assignment.')

    if request.method == 'GET':
        context = {'title': assignment.title, 'active_link': 'assignments'}

        professor = Professor.objects.filter(user=request.user).first()
        student = Student.objects.filter(user=request.user).first()

        if professor:
            questions = assignment.question_set.all()
            context['professor'] = professor
            context['form'] = QuestionCreateForm(
                assignment=assignment, auto_id=True)
            context['add'] = True

        elif student:
            questions = assignment.question_set.filter(draft=False)
            context['student'] = student

        context['assignment'] = assignment
        context['questions'] = questions

    # creating question
    elif request.method == 'POST':
        form = QuestionCreateForm(
            request.POST, assignment=assignment, auto_id=True)

        if form.is_valid():
            form.save()

            messages.success(request, 'Question added!')
            return redirect('app:assignment', pk=assignment.pk)

        else:
            context['form'] = form

    return render(request, 'app/cc-assignment.html', context)


@login_required
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
            return redirect('app:assignments')

        else:
            context['form'] = form
            return render(request, 'app/edit-assignment.html', context)


@login_required
def delete_assignment(request, pk):
    '''View to delete assignment.'''

    assignment = Assignment.objects.filter(pk=pk)
    assignment.delete()

    messages.success(request, 'Assignment deleted!')

    return redirect('app:assignments')


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


@login_required
def question(request, pk):
    question = Question.objects.filter(pk=pk).first()

    if not question:
        return HttpResponse('Invalid question!')

    context = {
        'title': question.title,
        'active_link': 'assignments',
        'question': question
    }

    professor = Professor.objects.filter(user=request.user).first()
    student = Student.objects.filter(user=request.user).first()

    if professor:
        context['professor'] = professor
        context['delete'] = True

    elif student:
        context['student'] = student

    return render(request, 'app/cc-question.html', context)


@login_required
def edit_question(request, pk):
    question = Question.objects.filter(pk=pk).first()

    if question is None:
        return HttpResponse('No valid question.')

    context = {
        'title': 'Edit Question',
        'question': question
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
            return redirect('app:question', pk=pk)

        else:
            context['form'] = form

            return render(request, 'app/edit-question.html', context)


@login_required
def delete_question(request, pk):
    question = Question.objects.filter(pk=pk).first()
    assignment = question.assignment
    question.delete()

    messages.success(request, 'Question deleted!')

    return redirect('app:assignment', pk=assignment.pk)


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
        query_class = Classroom.objects.filter(
            students__user__username=student)
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
        class_room = Classroom.objects.filter(
            students__user__username=student).first()
        assignments = Assignment.objects.filter(classroom=class_room)
        context = {
            'title': 'Assignments',
            'assignments': assignments
        }

    return render(request, 'app/assignment.html', context)
