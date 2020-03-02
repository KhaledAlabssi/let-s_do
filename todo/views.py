from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.
def signupuser(request):
	if request.method == 'GET':
		return render(request, 'todo/signupuser.html' , {'form': UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('current')
			except IntegrityError:
				return render(request, 'todo/signupuser.html' , {'form': UserCreationForm(), 'error': 'Username has already been token, Please choose new username'})
		else:
			return render(request, 'todo/signupuser.html' , {'form': UserCreationForm(), 'error': 'Password did not match!'})

def current(request):
	return render(request, 'todo/current.html')