from django.urls import path
from . import views
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', views.home, name="home page"),
    path('employee profile/<int:id>/', views.viewEmployee, name="view employee"),
    path('create employee/', views.createEmployee, name="create employee"),
    path('update employee/<int:id>/', views.updateEmployee, name="update employee"),
    path('delete employee/<int:id>/', views.deleteEmployee, name="delete employee"),
    path('create task/', views.createTask , name="create task"),
    path('update task/<int:id>/', views.updateTask, name="update task"),
    path('delete task/<int:id>/', views.deleteTask, name="delete task"),
    url('success/', success),
]