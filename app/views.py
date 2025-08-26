from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User,Note
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = hash_password(user.password)
            user.save()
            messages.success(request, 'User registered successfully!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_pass = hash_password(password)

        try:
            current_user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
            return redirect('login')

        if current_user.password == hashed_pass:
            request.session['user_id'] = current_user.id
            return redirect('home')
        else:
            messages.error(request, 'Invalid password')
            return redirect('login')

    return render(request, 'login.html')


def home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    current_user = User.objects.get(id=user_id)
    return render(request, 'home.html', {'user': current_user})





