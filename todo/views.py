from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm

# Create your views here.
def home(request):
	return render(request, 'todo/home.html')
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

def loginuser(request):
	if request.method == 'GET':
		return render(request, 'todo/login.html' , {'form': AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'User or password did not match'})
		else:
			login(request, user)
			return redirect('current')

def createtodo(request):
	if request.method == 'GET':
		return render(request, 'todo/createtodo.html' , {'form': TodoForm()})

	else:
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('current')
		except ValueError:
			return render(request, 'todo/createtodo.html' , {'form': TodoForm(), 'error': 'Bad input, try again!'})




def current(request):
	return render(request, 'todo/current.html')

def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')
