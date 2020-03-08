from pprint import pprint
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import forms


def index(request):
    return render(request, 'app/index.html')


def signup(request):
    context = dict()

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Signup Successful!')
            return redirect(reverse('app:login'))

        else:
            context['form'] = form
            return render(request, 'app/signup.html', context)

    elif request.method == 'GET':
        context['form'] = forms.SignupForm(auto_id=True)
        return render(request, 'app/signup.html', context)


def docs(request):
	return render(request, 'docs.html')
