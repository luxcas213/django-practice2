from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login , logout,authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{"form":UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # if not User.objects.filter(username=request.POST['username']).exists():
            #     user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
            #     user.save()
            #     login(request,user)
            #     return redirect('tasks')
            # else:
            #     return render(request, 'signup.html',{"form":UserCreationForm(),"error":"Username already exists"})
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError as e:
                return render(request, 'signup.html',{"form":UserCreationForm(),"error":"Username already exists"})

        else:
            return render(request, 'signup.html',{"form":UserCreationForm(),"error":"Passwords did not match"})
            

def home(request):
    return render(request, 'home.html')

def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html',{"tasks":tasks})


def signout(request):
    logout(request)
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{"form":AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{"form":AuthenticationForm(),"error":"Username or password is incorrect"})
        else:
            login(request,user)
            return redirect('tasks')

def createTask(request):
    if request.method=='GET':
        return render(request, 'create_Task.html',{"form":TaskForm()})
    else:
        try:
            newtask = Task.objects.create(title=request.POST['title'],description=request.POST['description'],important=bool(request.POST.get('important', False)),user=request.user)
            newtask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_Task.html',{"form":TaskForm(),"error":"Bad data passed in. Try again."})