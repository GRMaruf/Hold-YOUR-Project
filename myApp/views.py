from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myApp.models import *
from myApp.forms import *
from django.db.models import Q

@login_required
def home(request):
    return render(request, 'myApp/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if UserModel.objects.filter(username=username).exists():
            messages.warning(request, 'This username already exists.')
            return redirect('signup')

        if password != password2:
            messages.warning(request, 'Two passwords must be same.')
            return redirect('signup')
        
        UserModel.objects.create_user(
            username = username,
            password = password
        )
        messages.success(request, 'Registered successfully.')
        return redirect('signin')
    return render(request, 'master/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, 'Invalid credentials.')
            return redirect('signin')

        login(request, user)
        messages.success(request, 'Logged in successfully.')
        return redirect('home')
    return render(request, 'master/signin.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('signin')
    
@login_required
def my_projects(request):
    projects = Project.objects.filter(posted_by=request.user)
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(name__icontains = search) |
            Q(short_note__icontains = search) |
            Q(task_details__icontains = search)
        ).distinct()
    return render(request, 'myApp/my_projects.html', {'projects':projects})

@login_required
def delete_project(request, id):
    project = Project.objects.filter(id=id).first()
    if project is None:
        messages.error(request, f'The project with id-{id} not found. May be already deleted.')
        return redirect('my_projects')
    if project.posted_by != request.user:
        messages.error(request, f'This project (id-{id}) is not yours.')
        return redirect('my_projects')
    project.delete()
    messages.success(request, f'Project with id-{id} deleted successfully.')
    return redirect('my_projects')

@login_required
def view_project(request, id):
    project = Project.objects.filter(id=id).first()
    if project is None:
        messages.error(request, f'There is no project with id-{id}.')
        return redirect('my_projects')
    if project.posted_by != request.user:
        messages.error(request, f'This project (id-{id}) is not yours.')
        return redirect('my_projects')
    return render(request, 'myApp/view_project.html', {'project': project})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('view_project', form.id)
        else:
            # messages.error(request, f'ERROR: {form.errors}.')
            return render(request, 'myApp/project_form.html', {'form':form, 'status': 'Add New'})

    else:
        form = ProjectForm()
    return render(request, 'myApp/project_form.html', {'form':form, 'status': 'Add New'})

@login_required
def update_project(request, id):
    project = Project.objects.filter(id=id).first()
    if project is None:
        messages.error(request, f'There is no project with id-{id}.')
        return redirect('my_projects')
    if project.posted_by != request.user:
        messages.error(request, f'This project (id-{id}) is not yours.')
        return redirect('my_projects')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():
            form = form.save(commit=False)
            form.posted_by = request.user
            form.save()
            return redirect('view_project', form.id)
        else:
            return render(request, 'myApp/project_form.html', {'form':form, 'status': 'Update'})

    else:
        form = ProjectForm(instance = project)
    return render(request, 'myApp/project_form.html', {'form':form, 'status': 'Update'})


    