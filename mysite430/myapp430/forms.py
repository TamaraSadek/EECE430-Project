from django.forms import ModelForm
from .models import Employee, Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["employee", "description", "deadline", "points"]

    def __init__(self, *args, **kwargs):
        include_status = kwargs.pop('include_status', False)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        if not include_status:
            try:
                del self.fields['status']  # Exclude the status field if present
            except KeyError:
                pass




class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ["name", "phone", "email", "position", "team_id", "address"]