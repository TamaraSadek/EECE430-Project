from multiprocessing import Event
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import * 
from django.http import HttpResponseRedirect
from django.db import transaction
from django.conf import settings
import os
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import MoodForm, RegisterForm, EmployeeForm, SignUpForm
from .models import Employee, Task, Mood
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django import template
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# views.py
register = template.Library()

@register.filter(name='percentage')
def percentage(value, total):
    if total == 0:
        return 0
    return round((value / total) * 100, 2)

from .forms import BookingForm
from .models import Booking
from django.urls import reverse

def book_session(request): # book a wellness session with a well-being specialist

    # Assuming 'Well-being Specialist' is the desired position
    position = 'Well-being Specialist'
    
    # Get the specialist based on the position
    specialist = Employee.objects.filter(position=position).first()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # Assuming the logged-in user is the employee
            booking.employee = request.user
            booking.specialist = specialist
            booking.save()
            return redirect(reverse('booking_confirmation', kwargs={'booking_id': booking.booking_id}))
    else:
        form = BookingForm()
    
    return render(request, 'book_session.html', {'form': form})

from myapp430.models import Booking

def booking_confirmation(request, booking_id): # confirm your booking
    booking = Booking.objects.get(booking_id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

def loginPage(request): # login to a previously created account

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/') # home page
            else:
                form.add_error(None, 'Username or password incorrect.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logoutUser(request): # logout from currently signed in account
    logout(request)
    return redirect('login') #return to login page

from .forms import SignUpForm, EmployeeForm

def signup(request): # sign up into a new account (creating a user)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the newly created user
            return redirect('create employee')  # creating an employee from that user
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
    user_name = request.user.get_full_name() or request.user.username # Display logged in user's name
    employees = Employee.objects.all().order_by('employee_id') # Retrieve all employees
    tasks = Task.objects.all() # Retrieve all tasks
    events = Events.objects.all()  # Retrieve all events

    # Retrieve Task Completion Percentage
    total_employees = employees.count()
    total_tasks = tasks.count()
    complete_tasks = Task.objects.filter(status='Complete').count()
    pending_tasks = Task.objects.filter(status='In Progress').count()
    completion_percentage = totalCompletion()
    resources = Resource.objects.all() # Retrieve all resources


    # Iterate through all tasks and append them to the appropriate list
    # We now have in progress tasks listed first (in increasing order of deadline) followed by completed tasks
    in_progress_tasks = Task.objects.filter(status='In Progress').order_by('deadline')
    completed_tasks = Task.objects.filter(status='Complete')

    context = {
        'user_name': user_name,
        'employees': employees,
        'tasks': tasks,
        'events': events,  # Add events to the context
        'total_employees': total_employees,
        'total_tasks': total_tasks,
        'complete': complete_tasks,
        'in_progress': pending_tasks,  # Fix the key name to match the template
        'completion_percentage' : completion_percentage,
        'resources' :resources,
        'in_progress_tasks': in_progress_tasks,  # Add in_progress_tasks to the context
        'completed_tasks': completed_tasks,   
    }
    return render(request, 'myapp430/homepage.html', context)

def totalCompletion(): # compute percentage of tasks that have been completed (helper function)
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Complete').count()
    if total_tasks > 0:
        completion_percentage = (completed_tasks / total_tasks) * 100
    else:
        completion_percentage = 0
    return round(completion_percentage, 2)


# Employee Profile
def viewEmployee(request, id): # display all necessary features on employee profile
    employee = Employee.objects.get(employee_id=id) 
    tasks = Task.objects.filter(employees=employee)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Complete')
    tasks_in_progress = tasks.exclude(status='Complete')
    # Query mood data for the specific employee
    mood_entries = Mood.objects.filter(employee=employee)

    if total_tasks >0:
        percent_completed = round((completed_tasks.count() / total_tasks) * 100, 2)
    else:
        percent_completed = 0
        
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
        mood_percentages = {
            'Awful': 0,
            'Bad': 0,
            'Neutral': 0,
            'Good': 0,
            'Amazing': 0,
        }

    user = employee.user
    
    if not employee.user:
        context['upcoming_sessions'] = None
    else:
        upcoming_sessions = Booking.objects.filter(
            employee=employee.user,
            date__gte=timezone.now()
        ).order_by('date')

    
    context = {
        'employee': employee,
        'total_tasks':total_tasks,
        'tasks_in_progress': tasks_in_progress,
        'completed_tasks': completed_tasks,
        'percent_completed': percent_completed,
        'mood_entries': mood_entries, 
        'mood_percentages': mood_percentages,
        'upcoming_sessions': upcoming_sessions
    }
    return render(request, 'myapp430/employeeprofile.html', context)

# Employee Functions
def createEmployee(request): # create a new employee
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

def updateEmployee(request, id): # update employee info 
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

def deleteEmployee(request, id): # delete employee
    employee = Employee.objects.get(employee_id=id)
    if request.method == 'POST':
        employee.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':employee})


#Task Functions
def createTask(request): # create a new task, doesn't need to be assigned to any employee yet
    form = TaskForm()
    action = 'create'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/taskform.html', context)

def assignTask(request, id): # assign an existing task to an employee or group of employees
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

def updateTask(request, id): # update an existing task's information (deadline, assignee(s), etc.)
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

def deleteTask(request, id): # delete an existing task
    task = Task.objects.get(task_id=id)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':task})


# Events Functions
def addEvent(request): # add a new event
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

def updateEvent(request, id): # update an existing event's information
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

def deleteEvent(request, id): # delete an existing event
    Event = Events.objects.get(event_id=id)
    if request.method == 'POST':
        Event.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':Event})

#@login_required
def SignupEvent(request, id): # sign up to an event in the list
    event = Events.objects.get(event_id=id)

    if not request.user.is_authenticated or not hasattr(request.user, 'employee'):
        return JsonResponse({'error': 'User is not authenticated or does not have an associated employee'}, status=401)
    
    current_user = request.user

    # Check if the current employee is already registered for the event
    # Clicking on an event you already signed up for does nothing
    if EventRegistration.objects.filter(event=event, participant=current_user).exists():
        return redirect('/already_registered')

    # Create EventRegistration object for the current user and event
    # Clicking the sign up button automatically signs up the logged in user
    event_registration = EventRegistration(event=event, participant=current_user)
    event_registration.save()

    return JsonResponse({'message': 'Event signup successful'})

def already_registered(request):
    return render(request, 'myapp430/alreadyregistered.html')


# Mood Functions
def add_mood(request, employee_id): # input your current mood
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

def logo_image_view(request): # display logo on homepage
    image_path = os.path.join(settings.BASE_DIR, 'static', 'logo.png')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')
    

# Resources Functions
from .forms import ResourceForm
from .models import Resource
def create_resource(request): # create a new resource
    form = ResourceForm()
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/success')
    return render(request, 'myapp430/resource_form.html', {'form': form})

def update_resource(request, resource_id): # update an existing resource element
    resource = Resource.objects.get(resource_id=resource_id)
    form = ResourceForm(instance=resource)  # Pass the instance to the form
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    
    return render(request, 'myapp430/resource_form.html', {'form': form})

def delete_resource(request, resource_id): # delete an existing resource
    resource = Resource.objects.get(resource_id=resource_id)
    if request.method == 'POST':
        resource.delete()  # Delete the resource on POST
        return HttpResponseRedirect('/success')  # Redirect to success page or list
    
    return render(request, 'myapp430/deleteitem.html', {'item': resource})


# Team Functions
def createTeam(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/success')
    else:
        form = TeamForm()
    return render(request, 'myapp430/create_team.html', {'form': form})

# Successful Execution. Returned whenever any of the above functions executes successfully
def success(request):
    return render(request, 'myapp430/success.html')