from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from .models import Employee, Task, Goals, Mood, Events, Rewards, Team, EventRegistration
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add an email field

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

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
		fields = ["name", "phone", "email", "position", "team", "address"]

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
        fields = ["employee", "deadline","description","status"]

class MoodForm(ModelForm):
    class Meta:
        model = Mood
        fields = ['mood']
        widgets = {
            'mood': forms.Select(choices=Mood.STATUS),
        }

class RewardsForm(ModelForm):
    class Meta:
        model = Rewards
        fields = ["reward_name","description","stock","price"]

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["team_id", "description", "team_name"]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
