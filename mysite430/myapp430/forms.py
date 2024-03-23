from django.forms import ModelForm
from .models import Employee, Task

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = '__all__'

class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = '__all__'