from django.forms import forms
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import LoginForm, CustomUserModelFormRegister, \
    ChangePasswordModelForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

from .serializers import UserSerializer
from rest_framework import viewsets
from authentication.models import CustomUser


class UserAPIView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'authentication/login_info.html',
                                  {'messageSuccess': 'Authenticate successfully'})
                    # return HttpResponse('Authenticate successfully')
                else:
                    return render(request, 'authentication/login_info.html',
                                  {'message_err': 'Disabled account'})
                    # return HttpResponse('Disabled account')
            else:
                return render(request, 'authentication/login_info.html',
                              {'message_err': 'Invalid login'})
                # return HttpResponse('Invalid login')
        return render(request, 'authentication/login_info.html',
                      {'message_err': 'Invalid login'})
    else:
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserModelFormRegister(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password1'] == cd['password2']:
                user = CustomUser.create(email=cd['email'],
                                         password=cd['password1'],
                                         first_name=cd['first_name'],
                                         role=cd['role'],
                                         middle_name=cd['middle_name'],
                                         last_name=cd['last_name'])
                if not user:
                    return render(request, 'authentication/register.html',
                                  {'form_err': form.error_messages['incorrect_data']})

                return render(request, 'authentication/register_info.html',
                              {'messageSuccess': 'Success'})

            else:
                return render(request, 'authentication/register.html',
                              {'form_err': form.error_messages['password_mismatch'],
                               'form': form,})

        else:
            return render(request, 'authentication/register_info.html',
                          {'form_err': form.errors['email']})
    form = CustomUserModelFormRegister(initial={'email': "email@mail.com"},
                                       auto_id=False, label_suffix=':')
    return render(request, 'authentication/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')  # or return redirect('/some/url/')


# @permission_required('role')
def show_all_users(request):
    # if request.user.is_authenticated and request.user.role == 1:
    data = list(CustomUser.get_all())
    context = {'list_of_user': data}
    return render(request, 'users/users.html', context)


def role_of_user(request):
    if request.user.is_authenticated and request.user.role == 1:
        if request.method == 'POST':
            user_id = request.POST['data']
            if user_id:
                try:
                    data = get_object_or_404(CustomUser, id=user_id)
                    context = {'user': data,
                               'post': True}
                    return render(request, 'users/user_role.html', context)
                except AttributeError:
                    return render(request, 'users/user_role.html',
                                  {'user_by_id': "None user"})

    return render(request, 'users/user_role.html')


def main(request):
    return render(request, 'main/main.html')


@permission_required('role')
def update_user(request, user_id):
    from .forms import UpdateUserModelForm
    user = CustomUser.objects.get(id=user_id)
    form = UpdateUserModelForm(initial={
        'email': user.email,
        'first_name': user.first_name,
        'id': user.id,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'role': user.role,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
    })
    if request.method == 'POST':
        form = UpdateUserModelForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.id = user.id
            user_form.save()
        return redirect(reverse_lazy('authentication:users'))
    return render(request, 'users/update_user.html', {'form': form,
                                                     'user':user})


@permission_required('role')
def del_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect(reverse_lazy('authentication:users'))


@login_required
def change_password(request, user_id=None):
    form = ChangePasswordModelForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.get(id=user_id)
            # if cd['password2'] != user.password:
            #     return render(request, 'authentication/change_password.html',
            #                   {'form': form,
            #                    'error': 'Old password doesn\'t match'})
            # else:
            user.set_password(cd['new_password1'])
            user.save()
            return render(request, 'authentication/change_password.html',
                          {'form': form, 'resolt': '1'})

    return render(request, 'authentication/change_password.html',
                      {'form': form, })
