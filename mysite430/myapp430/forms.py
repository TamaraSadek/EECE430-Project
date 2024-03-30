from django.forms import ModelForm
from .models import Employee, Task,Goals, Mood,Events, Gifts,Team

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["employee", "description", "deadline", "points", "status"]


class EmployeeForm(ModelForm):
	class Meta:
		model = Employee
		fields = ["name", "phone", "email", "position", "team_id", "address"]

class GoalsForm(ModelForm):
    class Meta:
        model = Goals
        fields = ["goals_id","employee", "deadline","points","description","status","date_created"]

class MoodForm(ModelForm):
    class Meta:
        model = Mood
        fields = ["mood","employee", "date", "team_id"]
class EventsForm(ModelForm):
    class Meta:
        model = Events
        fields = ["event_name","participants","event_id","description","date","location"]
class GiftsForm(ModelForm):
    class Meta:
        model = Gifts
        fields = ["gift_name","description","stock","price"]
class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["team_id","members","description","team_name"]