from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegForm,EditUser
from .models import Tokens
from django.contrib.auth.models import User
from navbar.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from g_recaptcha.validate_recaptcha import validate_captcha
from uuid import uuid4
#REST_FRAMEWORK
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
user=get_user_model()
def index(request):
    return render(request,"base.html")

def forgotpass(request):
    if request.method =='POST':
        form=PasswordResetForm(data=request.POST)
        if form.is_valid():
            return redirect('index')
    form=PasswordResetForm()
    context = {'form': form,}
    return render(request, "forgot.html",context)
@validate_captcha
def NewUser(request):

    if request.method != 'POST':
        form = RegForm()
    else:
        form = RegForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('index')
    context = {'form': form,
    'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,}
    return render(request, "register.html",context)
def logout_view(request):
    logout(request)
    return redirect('index')
@login_required
def panel(request):
    if request.method =='POST':
        token= uuid4()
        try:
            Model=Tokens.objects.get(user=request.user)
            Model.delete()
        except:
            Model=Tokens.objects.create(user=request.user,token=token)
        tok=Model.token
        context={
        'token':tok
        }
        return render(request,"panel.html",context)
    else:
        try:
            Model=Tokens.objects.get(user=request.user)
            tok=Model.token
            context={
            'token':tok
            }

            if request.user.is_staff ==True:
                us=[]
                for i in user.objects.all():
                    us.append(str(i.username))
                context['users']=us
            return render(request,"panel.html",context)
        except:
            return render(request,"panel.html")
def delete(request):
    if request.user.is_staff ==True:
        us=user.objects.get(username=request.POST['user'])
        print(us)
        us.delete()
        return redirect('panel')
    return redirect('panel')
def change(request,username):
    form = EditUser()
    if request.user.is_staff ==True:
        if request.method != 'POST':
            form = EditUser()
        else:
            us=user.objects.get(username=username)
            form = EditUser(data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get("username")
                email=form.cleaned_data.get("email")
                password=form.cleaned_data.get("password1")
                if username!='':
                    us.username=username
                if email!='':
                    us.email=email
                if password!='':
                    us.username=password
                us.save()
                return redirect('panel')
    context = {'form': form,'username':str(username)}
    return render(request, "change.html",context)
@api_view(['GET','POST'])
def data(request):
    if request.method=='POST':

        try:
            token=request.data['token']

            Model=Tokens.objects.get(token=token)
            context={'user':str(Model.user.username),'email':str(Model.user.email)}

            return Response({'data':context})
        except:
            return Response({'data':"wrong token or something others :/"})
    return Response({'data':"wrong method"})
