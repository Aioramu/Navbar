from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegForm,EditUser
from .models import Tokens,Confirmation
from django.contrib.auth.models import User
from navbar.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from g_recaptcha.validate_recaptcha import validate_captcha
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from uuid import uuid4
#REST_FRAMEWORK
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
user=get_user_model()

def index(request):
    return render(request,"base.html")


@validate_captcha
def NewUser(request):

    if request.method != 'POST':
        form = RegForm()
    else:
        form = RegForm(data=request.POST)
        if form.is_valid():

            subject = 'Subject'


            recepient=form.cleaned_data.get("email")
            html_message = render_to_string('confirmaton.html', {'email':recepient,'domain':'0.0.0.0:8000'})
            message = strip_tags(html_message)
            #ail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False,html_message=html_message)
            new_user = form.save()
            login(request, new_user)
            con=Confirmation.objects.create(user=new_user)
            con.save()
            return redirect('index')
    context = {'form': form,
    'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,}
    return render(request, "register.html",context)
@login_required
def confirm(request):
    try:
        conf=Confirmation.objects.get(user=request.user)
        print(conf.confirm)
        conf.confirm=True
        conf.save()
        return render(request,"confirm_done.html")
    except:
        return redirect('login')
def logout_view(request):
    logout(request)
    return redirect('index')
@login_required
def panel(request):
    conf=Confirmation.objects.get(user=request.user)

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
        context['conf']=conf.confirm
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
            context['conf']=conf.confirm
            return render(request,"panel.html",context)
        except:

            context={'conf':conf.confirm}
            return render(request,"panel.html",context)
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
                try:
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
                except:
                    context = {'form': form,'username':str(username)}
                    return render(request, "change.html",context)
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
