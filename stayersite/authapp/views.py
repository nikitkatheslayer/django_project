import time

from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserCheckForm
from django.contrib import auth

from authapp.models import ShopUser
from authapp.serializers import ShopUsersSerializer
from django.contrib import messages
import hashlib

def create_hash_password(password):
    salt = 'qaz'.encode()
    pas = password.encode()
    dk = hashlib.pbkdf2_hmac('sha1', pas, salt, 100000)
    return dk.hex()

def check_pass(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        hash_password1 = create_hash_password(password1)
        hash_password2 = create_hash_password(password2)
        print(hash_password1, hash_password2)
        if hash_password1 != hash_password2:
            messages.success(request, 'Пароли не совпадают')
            messages.success(request, f'Хэш первого пароля: {hash_password1}')
            messages.success(request, f'Хэш второго пароля: {hash_password2}')
        else:
            messages.error(request, 'Пароли совпадают')
            messages.error(request, f'Хэш первого пароля: {hash_password1}')
            messages.error(request, f'Хэш второго пароля: {hash_password2}')

    return render(request, 'authapp/checkpass.html')

def login(request):
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            print('User is Valid')
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        form = ShopUserLoginForm()

    context = {
        'form': form,
    }
    print(request.POST)
    return render(request, 'authapp/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))

def register(request):
    title = 'Регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            if ShopUser.objects.filter(username=user.username).exists():
                messages.error(request, 'Пользователь с таким логином уже существует.')
                return HttpResponseRedirect(reverse('authapp:register'))
            user.save()
            messages.success(request, 'Пользователь успешно зарегистрирован. Пожалуйста, войдите.')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        register_form = ShopUserRegisterForm()
    content = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/register.html', content)

class ShopUserAPIView(APIView):
    def get(self, request):
        lst = ShopUser.objects.all()
        return Response({'user_info': ShopUsersSerializer(lst, many=True).data})

    def post(self, request):
        serializer = ShopUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_new = ShopUser.objects.create_user(
            username=request.data['username'],
            password=request.data['password']
        )

        return Response({'user_info': ShopUsersSerializer(post_new).data})

