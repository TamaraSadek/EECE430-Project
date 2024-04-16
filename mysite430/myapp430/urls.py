from django.urls import path, include
from . import views
##from django.conf.urls import url
from django.urls import re_path as url
from .views import *
from .views import login
from django.contrib.auth.views import LogoutView
from .views import register



urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name="home page"),
    path('employee profile/<int:id>/', views.viewEmployee, name="view employee"),\
    path('add-mood/<int:employee_id>/', add_mood, name='add mood'),
    #path('add mood/<int:id>/', addMood, name="add mood"),
    path('create employee/', views.createEmployee, name="create employee"),
    path('update employee/<int:id>/', views.updateEmployee, name="update employee"),
    path('delete employee/<int:id>/', views.deleteEmployee, name="delete employee"),
    path('create task/', views.createTask , name="create task"),
    path('assign task/<int:id>/', views.assignTask , name="assign task"),
    path('update task/<int:id>/', views.updateTask, name="update task"),
    path('delete task/<int:id>/', views.deleteTask, name="delete task"),
    path('add event/',views.addEvent,name="add event"),
    path('update event/<int:id>/', views.updateEvent,name="update Event"),
    path('delete event/<int:id>/', views.deleteEvent, name="delete event"),
    path('signup event/<int:id>/', views.SignupEvent, name="Signup event"),
    path('register/', register, name='register'),
    url('success/', success),
    path('logo/', views.logo_image_view, name='logo_image'),]