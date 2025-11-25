from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def home(request):
    todos = Todo.objects.filter(user=request.user).order_by('-date')
    return render(request, "todos/home.html", {"todos": todos})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Validate empty fields
        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return render(request, "todos/signup.html")
        # Check existing user
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "todos/signup.html")
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created! Please login.")
        return redirect("signin")  # MUST RETURN
    return render(request, "todos/signup.html")

    
def signin(request):
    if request.method == "POST":
        uname = request.POST.get("username")  # match with form input name
        password = request.POST.get("password")
        user = authenticate(request, username=uname, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')     # OR 'create_todo'
        else:
            messages.error(request, "Invalid username or password")
            return redirect('signin')
    return render(request, 'todos/login.html')


def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def create_todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        Todo.objects.create( user= request.user, title = title)
        return redirect("home")
    return render(request, 'todos/create.html')

@login_required
def edit_todo(request,id):
    todo = get_object_or_404(Todo, id=id, user = request.user )
    if request.method == "POST":
        todo.title = request.POST.get("title")
        todo.status = request.POST.get("status") == "on"
        todo.save()
        return redirect('home')
    return render(request, "todos/edit.html", {"todo":todo})

@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id, user=request.user)
    todo.delete()
    return redirect('home')

