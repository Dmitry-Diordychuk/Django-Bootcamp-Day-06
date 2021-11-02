from django import forms
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth

from django.conf import settings
import random
from .forms import LoginForm, RegisterForm
from .models import User

def get_username(request):
	if request.user.is_authenticated:
		username = request.user.username
	else:
		username = request.session.get('username')
		if not username:
			request.session['username'] = random.choice(settings.USERS_NAMES)
			request.session.save()
			username = request.session.get('username')
	return username

# Create your views here.
def home(request):

	return render(request, 'ex/home.html', {
		'username': get_username(request)
	})

def login(request):
	if request.user.is_authenticated:
		return redirect('home')

	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = auth.authenticate(request, username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('home')
	return render(request, 'ex/login.html', {
		'username': get_username(request),
		'form': form
	})

def register(request):
	if request.user.is_authenticated:
		return redirect('home')

	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = User.objects.create_user(
				username,
				'',
				password,
			)
			user.save()
			user = auth.authenticate(request, username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('home')
	return render(request, 'ex/register.html', {
		'username': get_username(request),
		'form': form,
	})

def logout(request):
	if not request.user.is_authenticated:
		return redirect('home')
	auth.logout(request)
	return redirect('home')
