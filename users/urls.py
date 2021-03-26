from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
#app_name='users'
urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('registration', views.NewUser, name='register'),
    path('log', views.logout_view, name='log'),
    path('reset',views.forgotpass,name='reset'),

    #path('lk',views.lk,name='lk')
    ]
