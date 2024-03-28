from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import * 
from django.http import HttpResponseRedirect

# Home Page
def home(request):
    employees = Employee.objects.all().order_by('employee_id')
    tasks = Task.objects.all()
    total_employees = employees.count()
    total_tasks = tasks.count()
    complete_tasks = Task.objects.filter(status=1).count()
    pending_tasks = Task.objects.filter(status=0).count()

    context = {'employees':employees, 'tasks':tasks,
	'total_employees':total_employees,'total_tasks':total_tasks, 
	'complete':complete_tasks, 'in Progress':pending_tasks}
    return render(request, 'myapp430/homepage.html', context)

# Employee Profile
def viewEmployee(request, id):
    employee = Employee.objects.get(employee_id=id)
    tasks = Task.objects.filter(employee=employee)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=1).count()
    if total_tasks > 0:
        percent_completed = (completed_tasks / total_tasks) * 100
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
            formdata = form.cleaned_data
            form.save()
            return HttpResponseRedirect('/success')
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/taskform.html', context)


# update task
def updateTask(request, id):
    action = 'update'
    task = Task.objects.get(task_id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, include_status=True)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success')
    else:
        form = TaskForm(instance=task, include_status=True)
    context = {'action':action, 'form':form}
    return render(request, 'myapp430/taskform.html', context)








# delete task
def deleteTask(request, id):
    task = Task.objects.get(task_id=id)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect('/success')
    return render(request, 'myapp430/deleteitem.html', {'item':task})

# Successful Execution
def success(request):
    return render(request, 'myapp430/success.html')