# Install Django if you haven't
# pip install django

# Create a new Django project
# django-admin startproject todoproject

# Navigate into the project and create an app
# cd todoproject
# python manage.py startapp todo

# settings.py (add 'todo' to INSTALLED_APPS)

# models.py (Define Task model)
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# forms.py (Form for adding tasks)
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'completed']

# views.py (Handle task CRUD operations)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

# urls.py (Map views to URLs)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]

# templates/todo/task_list.html (Basic UI)
"""
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
</head>
<body>
    <h2>Welcome, {{ request.user.username }}</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Task</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>{{ task.title }} - <a href="{% url 'delete_task' task.id %}">Delete</a></li>
        {% endfor %}
    </ul>
    <a href="{% url 'logout' %}">Logout</a>
</body>
</html>
"""

# Authentication (in main urls.py of project)
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
