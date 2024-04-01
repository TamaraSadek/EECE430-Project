from multiprocessing import Event
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import * 
from django.http import HttpResponseRedirect
from django.db import transaction

# Home Page
def home(request):
    employees = Employee.objects.all().order_by('employee_id')
    tasks = Task.objects.all()
    events = Events.objects.all()  # Retrieve all events
    total_employees = employees.count()
    total_tasks = tasks.count()
    complete_tasks = Task.objects.filter(status='Complete').count()
    pending_tasks = Task.objects.filter(status='In Progress').count()

    context = {
        'employees': employees,
        'tasks': tasks,
        'events': events,  # Add events to the context
        'total_employees': total_employees,
        'total_tasks': total_tasks,
        'complete': complete_tasks,
        'in_progress': pending_tasks,  # Fix the key name to match the template
    }
    return render(request, 'myapp430/homepage.html', context)

# Employee Profile
def viewEmployee(request, id):
    employee = Employee.objects.get(employee_id=id)
    tasks = Task.objects.filter(employee=employee)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Complete').count()
    if total_tasks > 0:
        percent_completed = round((completed_tasks / total_tasks) * 100, 2)
    else:
        percent_completed = 0
    context = {'employee':employee, 'tasks':tasks, 'total_tasks':total_tasks, 'completed_tasks': completed_tasks, 'percent_completed': percent_completed}
    return render(request, 'myapp430/employeeprofile.html', context)

    
# Employee Functions
# create employee
def createEmployee(request):
    form = EmployeeForm()
    action = 'create'
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            ''''
            instead of doing all of this, we will use form.save() method

            name = formdata['name']
            phone = formdata['phone']
            email = formdata['email']
            position = formdata['position']
            team_id = formdata['team_id']
            address = formdata['address']
            Employee.objects.create(name=name,phone=phone,email=email,position=position,team_id=team_id,address=address)
            '''
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/employeeform.html', context)

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
# assign task
def createTask(request):
    form = TaskForm()
    action = 'create'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            task = form.instance 
            if task.status == 'Complete' and task.credited == False:
                employee = task.employee
                with transaction.atomic():
                    employee.points += task.points
                    task.credited = True
                    employee.save()
                    task.save()
            return HttpResponseRedirect('/success')
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

# Successful Execution
def success(request):
    return render(request, 'myapp430/success.html')