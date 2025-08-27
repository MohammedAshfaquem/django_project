from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, NoteForm
from .models import User, Note
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
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


 
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = hash_password(request.POST['password'])
        try:
            user = User.objects.get(email=email)
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('note_list')
        except User.DoesNotExist:
            pass
        return redirect('user_login')
    return render(request, 'login.html')



def user_logout(request):
    request.session.flush()
    return redirect('user_login')

# Create Note
def create_note(request):
    user_id = request.session['user_id']
    current_user = get_object_or_404(User,id=user_id)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = current_user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form})

# Read Notes
def note_list(request):
    user_id = request.session['user_id']
    current_user = get_object_or_404(User, id=user_id)
    notes = Note.objects.filter(user=current_user)
    return render(request, 'note_list.html', {'notes': notes, 'user': current_user})

# Update Note
def update_note(request, pk):
    user_id = request.session['user_id']
    current_user = get_object_or_404(User, id=user_id)
    note = get_object_or_404(Note, pk=pk, user=current_user)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'note_form.html', {'form': form})

# Delete Note
def delete_note(request, pk):
    user_id = request.session['user_id']
    current_user = get_object_or_404(User, id=user_id)
    note = get_object_or_404(Note, pk=pk, user=current_user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'confirm_delete.html', {'note': note})
