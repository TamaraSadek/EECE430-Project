from django.urls import path, include
from . import views
##from django.conf.urls import url
from django.urls import re_path as url
from .views import *
from .views import login
from django.contrib.auth.views import LogoutView
from .views import register
from .views import signup



urlpatterns = [
    path('signup/', signup, name='signup'),
    path('register/', register, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('', views.home, name="home page"),

    path('employee profile/<int:id>/', views.viewEmployee, name="view employee"),\
    path('add-mood/<int:employee_id>/', add_mood, name='add mood'),
    path('create employee/', views.createEmployee, name="create employee"),
    path('update employee/<int:id>/', views.updateEmployee, name="update employee"),
    path('delete employee/<int:id>/', views.deleteEmployee, name="delete employee"),

    path('create task/', views.createTask , name="create task"),
    path('assign task/<int:id>/', views.assignTask , name="assign task"),
    path('update task/<int:id>/', views.updateTask, name="update task"),
    path('delete task/<int:id>/', views.deleteTask, name="delete task"),
    path('already registered/', views.already_registered, name="already registered"),

    path('add event/', views.addEvent, name="add event"),
    path('update event/<int:id>/', views.updateEvent,name="update Event"),
    path('delete event/<int:id>/', views.deleteEvent, name="delete event"),
    path('signup_event/<int:id>/', views.SignupEvent, name="Signup_event"),

    path('create_resource/', views.create_resource, name='create_resource'),
    path('update_resource/<int:resource_id>/', views.update_resource, name='update_resource'),
    path('delete_resource/<int:resource_id>/', views.delete_resource, name='delete_resource'),
    
    path('create_team/', views.createTeam, name='create_team'),

    path('book_session/', book_session, name='book_session'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),

    url('success/', success),
    path('logo/', views.logo_image_view, name='logo_image'),]