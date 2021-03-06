from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
#app_name='users'
urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('registration', views.NewUser, name='register'),
    path('log', views.logout_view, name='log'),
    path('panel',views.panel,name='panel'),
    path('delete',views.delete,name='delete'),
    path('change/<username>/',views.change,name='change'),
    path('verification/', include('verify_email.urls')),
    path('confirm',views.confirm,name='confirm'),
    url(r'^person/$',views.data,name='person'),
    ]
