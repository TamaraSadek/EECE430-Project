from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from .models import Employee, Task, Mood, Events, Rewards, Team, EventRegistration, Resource
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Booking


from .models import Employee

class SignUpForm(UserCreationForm): # used for signing up
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm): # used for logging in
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = ['username', 'password']

class TaskForm(ModelForm): # used for creating/updating a task
    class Meta:
        model = Task
        fields = ["employees", "description", "deadline", "points", "status"]

class TaskAssignment(ModelForm): # used for assigning a task
     class Meta:
          model = Task
          fields = ["employees"]

class EmployeeForm(ModelForm): # used for creating/updating an employee
	class Meta:
		model = Employee
		fields = ["name", "phone", "email", "position", "team", "address"]

class EventsForm(ModelForm): # used for creating/updating an event
    class Meta:
        model = Events
        fields = ['event_name', 'description', 'date', 'location']
        widgets = {
            'participants': CheckboxSelectMultiple,  # Render as checkboxes for multiple selection
        }

class MoodForm(ModelForm): # used for adding a mood
    class Meta:
        model = Mood
        fields = ['mood']
        widgets = {
            'mood': forms.Select(choices=Mood.STATUS),
        }

class RewardsForm(ModelForm): # used for adding a reward in the shop -- not implemented yet
    class Meta:
        model = Rewards
        fields = ["reward_name","description","stock","price"]

class TeamForm(ModelForm): # used for adding/updating a team -- not implemented yet
    class Meta:
        model = Team
        fields = ["team_id", "team_name", "description"]

class ResourceForm(ModelForm): # used for adding/updating a resource
    class Meta:
        model = Resource
        fields = ["resource_name", "resource_description", "link"]

from .models import Booking, Employee

class BookingForm(forms.ModelForm): # used for creating a booking for wellness session
    def __init__(self, *args, **kwargs):
        position = kwargs.pop('position', None)
        super().__init__(*args, **kwargs)
        if position:
            self.fields['specialist'].queryset = Employee.objects.filter(position=position)

    class Meta:
        model = Booking
        fields = ['employee', 'specialist', 'date', 'time', 'is_confirmed']

