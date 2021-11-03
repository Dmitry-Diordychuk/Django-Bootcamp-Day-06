from django import forms
from django.http.response import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.contrib import auth

from django.conf import settings
import random
from .forms import LoginForm, RegisterForm, TipForm
from .models import User, Tip

def get_username(request):
	if request.user.is_authenticated:
		username = request.user.username
	else:
		username = request.session.get('username')
		if not username:
			request.session['username'] = random.choice(settings.USERS_NAMES)
			username = request.session.get('username')
			request.session.save()
	return username

# Create your views here.
def home(request):
	form = TipForm()
	if request.method == 'POST' and request.user.is_authenticated:
		form = TipForm(request.POST)
		if form.is_valid():
			tip = form.save(commit=False)
			tip.author = request.user
			tip.save()
			form = TipForm()

	tips = Tip.objects.all()
	return render(request, 'ex/home.html', {
		'username': get_username(request),
		'form': form,
		'tips': tips,
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
				request.session.set_expiry(0)
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

def vote(request, pk):
	if not request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		upvote = request.POST.get('upvote')
		downvote = request.POST.get('downvote')
		tip = Tip.objects.get(pk=pk)
		if not tip:
			raise Http404("Tip does not exist")
		if upvote:
			if request.user in tip.upvotes.all():
				tip.upvotes.remove(request.user)
			else:
				tip.upvotes.add(request.user)
				tip.downvotes.remove(request.user)
			tip.save()
		elif downvote:
			if request.user in tip.downvotes.all():
				tip.downvotes.remove(request.user)
			else:
				tip.downvotes.add(request.user)
				tip.upvotes.remove(request.user)
			tip.save()

	return redirect('home')


def delete(request, pk):
	if not request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		tip = Tip.objects.get(pk=pk)
		if not tip:
			raise Http404("Tip does not exist")
		tip.delete()
	return redirect('home')
