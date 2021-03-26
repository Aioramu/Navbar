from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegForm
from django.contrib.auth.models import User
from navbar.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from g_recaptcha.validate_recaptcha import validate_captcha
# Create your views here.
def index(request):
    return render(request,"base.html")

def forgotpass(request):
    if request.method =='POST':
        form=PasswordResetForm(data=request.POST)
        if form.is_valid():
            return redirect('users:index')
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
            return redirect('users:index')
    context = {'form': form,
    'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,}
    return render(request, "register.html",context)
def logout_view(request):
    logout(request)
    return redirect('users:index')
