from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm
from django.contrib import auth

from authapp.models import ShopUser
from authapp.serializers import ShopUsersSerializer


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
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
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
# class ShopUserAPIView(generics.ListAPIView):
#     queryset = ShopUser.objects.all()
#     serializer_class = ShopUsersSerializer
