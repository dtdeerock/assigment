from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserCreationForm, UserLoginForm, DocFileForm
from .models import User, DocFile


def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'index.html')

def user_chat(request):
    return render(request, 'chat.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin:
                    return redirect('admin_panel')
                else:
                    return redirect('user_panel')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def admin_panel(request):
    if not request.user.is_admin:
        return redirect('user_panel')
    if request.method == 'POST':
        form = DocFileForm(request.POST, request.FILES)
        if form.is_valid():
            doc_file = form.save(commit=False)
            doc_file.user = request.user
            doc_file.save()
            messages.success(request, 'The file has been uploaded successfully.')
            return redirect('admin_panel')
    else:
        form = DocFileForm()
    files = DocFile.objects.all()
    return render(request, 'admin_panel.html', {'form': form, 'files': files})

@login_required
def user_panel(request):
    if request.user.is_admin:
        return redirect('admin_panel')
    return render(request, 'user_panel.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
