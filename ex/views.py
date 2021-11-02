from django.http.response import HttpResponse
from django.shortcuts import render

from django.conf import settings
import random

# Create your views here.
def home(request):
	if not request.session.get('username'):
		request.session['username'] = random.choice(settings.USERS_NAMES)
	return render(request, 'ex/home.html', {
		'username': request.session.get('username')
	})
