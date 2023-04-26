from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import RegisterUserForm, UserUpdateForm


# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_superuser


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('home')
        else:
            messages.success(request, "Wrong Username or Password")
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Log Out Successful!")
    return redirect('home')


@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        user_form = UserUpdateForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile_settings')

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_settings')

    else:
        password_form = PasswordChangeForm(user)
        user_form = UserUpdateForm(instance=user)

    context = {
        'user': user,
        'password_form': password_form,
        'user_form': user_form,
    }

    return render(request, 'authenticate/profile_settings.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
    else:
        return render(request, 'authenticate/delete_account.html')


@login_required
@user_passes_test(is_admin)
def users_list(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'authenticate/user_list.html', context)


@user_passes_test(is_admin)
@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {
        'user': user,
    }
    return render(request, 'authenticate/user_detail.html', context)


@login_required
@user_passes_test(is_admin)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        password_form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid() and password_form.is_valid():
            user = form.save(commit=False)
            password = password_form.cleaned_data['new_password1']
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, 'The profile was successfully updated!')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=user)
        password_form = SetPasswordForm(user=user)
    context = {
        'user': user,
        'form': form,
        'password_form': password_form,
    }
    return render(request, 'authenticate/edit_user.html', context)


@user_passes_test(is_admin)
@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')
    return render(request, 'delete_user.html', {'user': user})
