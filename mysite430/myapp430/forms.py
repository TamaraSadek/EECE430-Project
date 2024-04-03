from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Employee, Task,Goals, Mood,Events, Gifts,Team

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["employees", "description", "deadline", "points", "status"]

class TaskAssignment(ModelForm):
     class Meta:
          model = Task
          fields = ["employees"]

class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ["name", "phone", "email", "position", "team_id", "address"]

class EventsForm(ModelForm):
    class Meta:
        model = Events
        fields = ['event_name', 'description', 'date', 'location']
        widgets = {
            'participants': CheckboxSelectMultiple,  # Render as checkboxes for multiple selection
        }

class GoalsForm(ModelForm):
    class Meta:
        model = Goals
        fields = ["goal_id","employee", "deadline","points","description","status"]

class MoodForm(ModelForm):
    class Meta:
        model = Mood
        fields = ["mood","employee", "team_id"]

class GiftsForm(ModelForm):
    class Meta:
        model = Gifts
        fields = ["gift_name","description","stock","price"]

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["team_id","members","description","team_name"]