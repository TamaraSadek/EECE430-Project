from multiprocessing import Event
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import * 
from django.http import HttpResponseRedirect
from django.db import transaction
from django.conf import settings
import os

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import MoodForm
from .models import Employee, Task, Mood
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django import template
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .forms import EmployeeForm, SignUpForm




register = template.Library()

@register.filter(name='percentage')
def percentage(value, total):
    if total == 0:
        return 0
    return round((value / total) * 100, 2)



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if Employee.objects.filter(user=user).exists():
                return redirect('/')  # Redirect to homepage or dashboard
            else:
                # Redirect to employee creation page
                return redirect('create employee')  # Make sure you have a URL named 'createEmployee'
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from .forms import SignUpForm, EmployeeForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the newly created user
            return redirect('create employee')  # Redirect to the employee profile creation
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create an Employee instance for the new user
            Employee.objects.create(user=user)
            return redirect('login')  # Redirect them to the login page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# Home Page
def home(request):
    employees = Employee.objects.all().order_by('employee_id')
    tasks = Task.objects.all()
    events = Events.objects.all()  # Retrieve all events
    total_employees = employees.count()
    total_tasks = tasks.count()
    complete_tasks = Task.objects.filter(status='Complete').count()
    pending_tasks = Task.objects.filter(status='In Progress').count()
    completion_percentage = totalCompletion()
    context = {
        'employees': employees,
        'tasks': tasks,
        'events': events,  # Add events to the context
        'total_employees': total_employees,
        'total_tasks': total_tasks,
        'complete': complete_tasks,
        'in_progress': pending_tasks,  # Fix the key name to match the template
        'completion_percentage' : completion_percentage,
    }
    return render(request, 'myapp430/homepage.html', context)

# Employee Profile
def viewEmployee(request, id):
    employee = Employee.objects.get(employee_id=id)
    tasks = Task.objects.filter(employees=employee)
    total_tasks = tasks.count()
    #completed_tasks = tasks.filter(status='Complete').count()
    completed_tasks = tasks.filter(status='Complete')
    tasks_in_progress = tasks.exclude(status='Complete')
    # Query mood data for the specific employee
    mood_entries = Mood.objects.filter(employee=employee)

    if total_tasks >0:
        percent_completed = round((completed_tasks.count() / total_tasks) * 100, 2)
    else:
        percent_completed = 0
    #context = {'employee':employee, 'tasks':tasks, 'total_tasks':total_tasks, 'completed_tasks': completed_tasks, 'percent_completed': percent_completed}
    
    '''# Calculate percentage of recent mood entries for each mood category
    mood_entries = Mood.objects.filter(employee=employee)
    recent_mood_entries = mood_entries.order_by('-date')
    mood_count = recent_mood_entries.count()
    recent_mood_entries = recent_mood_entries[:10]  # Consider the 10 most recent mood entries
    mood_analytics = {
        'very_bad': recent_mood_entries.filter(mood='Very bad').count() / mood_count * 100,
        'bad': recent_mood_entries.filter(mood='Bad').count() / mood_count * 100,
        'neutral': recent_mood_entries.filter(mood='Neutral').count() / mood_count * 100,
        'good': recent_mood_entries.filter(mood='Good').count() / mood_count * 100,
        'very_good': recent_mood_entries.filter(mood='Very good').count() / mood_count * 100,
        }'''
    
    '''
    # Calculate percentage of recent mood entries for each mood category
    mood_entries = Mood.objects.filter(employee=employee).order_by('-date')[:10]  # Get the 10 most recent mood entries
    # Count the total number of recent mood entries
    total_recent_mood_entries = mood_entries.count()
    # Calculate the percentage of each mood category among the recent mood entries
    mood_counts = mood_entries.values('mood').annotate(count=Count('mood'))
    mood_analytics = {}
    for mood_count in mood_counts:
        mood_analytics[mood_count['mood']] = (mood_count['count'] / total_recent_mood_entries) * 100'''
        
    '''
    # Calculate mood analytics
    mood_analytics = mood_entries.values('mood').annotate(count=Count('id'))
    total_moods = mood_entries.count()
    mood_percentages = {}
    for mood in Mood.STATUS:
        mood_name = mood[0]
        mood_count = mood_analytics.filter(mood=mood_name).first()
    if mood_count is not None:
        count = mood_count['count']
        mood_percentages[mood_name] = round((count / total_moods) * 100, 2)
    else:
        mood_percentages[mood_name] = 0'''
        
    '''
    # Calculate mood percentages
    mood_counts = mood_entries.values('mood').annotate(count=Count('mood'))
    total_moods = mood_entries.count()
    mood_percentages = {}
    for mood_count in mood_counts:
        mood_percentages[mood_count['mood']] = round((mood_count['count'] / total_moods) * 100, 2)
        '''
    
    # Calculate mood percentages
    total_moods = mood_entries.count()
    mood_percentages = {}
    if total_moods > 0:
        mood_percentages = {
            'Awful': round((mood_entries.filter(mood='Awful').count() / total_moods) * 100, 2),
            'Bad': round((mood_entries.filter(mood='Bad').count() / total_moods) * 100, 2),
            'Neutral': round((mood_entries.filter(mood='Neutral').count() / total_moods) * 100, 2),
            'Good': round((mood_entries.filter(mood='Good').count() / total_moods) * 100, 2),
            'Amazing': round((mood_entries.filter(mood='Amazing').count() / total_moods) * 100, 2),
        }
    else:
    # If there are no mood entries, set all mood percentages to 0
        mood_percentages = {
            'Awful': 0,
            'Bad': 0,
            'Neutral': 0,
            'Good': 0,
            'Amazing': 0,
        }




    
    context = {
        'employee': employee,
        'total_tasks':total_tasks,
        'tasks_in_progress': tasks_in_progress,
        'completed_tasks': completed_tasks,
        'percent_completed': percent_completed,
        'mood_entries': mood_entries, # Include mood data in the context
        'mood_percentages': mood_percentages,
        # Add other context variables as needed
    }
    return render(request, 'myapp430/employeeprofile.html', context)

def totalCompletion():
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Complete').count()
    if total_tasks > 0:
        completion_percentage = (completed_tasks / total_tasks) * 100
    else:
        completion_percentage = 0
    return round(completion_percentage, 2)

# Employee Functions
# create employee

#def createEmployee(request):
 #   form = EmployeeForm()
  #  action = 'create'
   # if request.method == 'POST':
    #    form = EmployeeForm(request.POST)
     #   if form.is_valid():
      #      formdata = form.cleaned_data
       #     form.save()
        #    return HttpResponseRedirect('/success')
    #context = {'action':action, 'form':form}
    #return render(request, 'myapp430/employeeform.html', context)
def createEmployee(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if Employee.objects.filter(user=request.user).exists():
        return redirect('view employee')
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user  # Link employee to the logged-in user
            employee.save()
            return HttpResponseRedirect('/success')  
    return render(request, 'myapp430/employeeform.html', {'form': form})
# update employee info 
def updateEmployee(request, id):
    action = 'update'
    employee = Employee.objects.get(employee_id = id)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/employeeform.html', context)

# delete employee
def deleteEmployee(request, id):
    employee = Employee.objects.get(employee_id=id)
    if request.method == 'POST':
        employee.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':employee})


#Task Functions
#create task
def createTask(request):
    form = TaskForm()
    action = 'create'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/taskform.html', context)

# assign task
def assignTask(request, id):
    action = 'assign'
    task = Task.objects.get(task_id=id)
    if request.method == 'POST':
        form = TaskAssignment(request.POST, instance = task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    else:
        form = TaskAssignment(instance=task)
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/taskform.html', context)

# update task
def updateTask(request, id):
    action = 'update'
    task = Task.objects.get(task_id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if form.cleaned_data['status'] == 'Complete' and task.credited == False:
                with transaction.atomic():
                    task.employee.points +=  form.cleaned_data['points']
                    task.credited = True
                    task.employee.save()
                    task.save()
            return HttpResponseRedirect('/success')
    else:
        form = TaskForm(instance=task)
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/taskform.html', context)

# delete task
def deleteTask(request, id):
    task = Task.objects.get(task_id=id)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':task})


# Events Functions
# Add Event
def addEvent(request):
    form = EventsForm()
    action = 'create'
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/createevent.html', context)

#Update Event
def updateEvent(request, id):
    action = 'update'
    Event = Events.objects.get(event_id = id)
    form = EventsForm(instance=Event)

    if request.method == 'POST':
        form = EventsForm(request.POST, instance=Event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/createevent.html', context)

#delete event
def deleteEvent(request, id):
    Event = Events.objects.get(event_id=id)
    if request.method == 'POST':
        Event.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':Event})

'''
def SignupEvent(request, id):
    event = Events.objects.get(event_id=id)
    form = EventsForm()  # Create an empty form
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            current_employee = request.user.employee
            event.participants.add(current_employee)
            return HttpResponseRedirect('/success')

    context = {'form': form, 'event': event}  # Pass the form and event to the template
    return render(request, 'myapp430/signupevent.html', context)
'''
#@login_required
def SignupEvent(request, id):
    event = Events.objects.get(event_id=id)
    current_user = request.user.employee# Retrieve the Employee instance associated with the current user
    form = EventRegistrationForm()  # Create an empty form
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            # check if the current employee is already registered for the event
            #if EventRegistration.objects.filter(event=event, participant=current_employee).exists():
                # handle the case where the employee is already registered
                #return HttpResponseRedirect('/already_registered') 
    
            event_registration = EventRegistration(event=event, participant=current_user)
            event_registration.save()
            return HttpResponseRedirect('/success')
 
    context = {'form': form, 'event': event}  # Pass the form and event to the template
    return render(request, 'myapp430/signupevent.html', context)

'''def addMood(request, id):
    if request.method == 'POST':
        employee = Employee.objects.get(employee_id=id)
        mood_form = MoodForm(request.POST)
        if mood_form.is_valid():
            mood_instance = mood_form.save(commit=False)
            mood_instance.employee = employee
            mood_instance.save()
            return redirect('view employee', id=id)
    else:
        mood_form = MoodForm()
    return render(request, 'myapp430/mood_form.html', {'form': mood_form})'''

def add_mood(request, employee_id):
    employee = Employee.objects.get(employee_id=employee_id)
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.employee = employee
            mood.save()
            return redirect('view employee', id=employee_id)
    else:
        form = MoodForm()
    return render(request, 'myapp430/mood_form.html', {'form': form})

def logo_image_view(request):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'logo.png')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')
    


# Successful Execution
def success(request):
    return render(request, 'myapp430/success.html')

