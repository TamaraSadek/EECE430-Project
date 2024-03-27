from django.forms import ModelForm
from .models import Employee, Task

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ["employee", "description", "deadline", "points"]

class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ["name", "phone", "email", "position", "team_id", "address"]