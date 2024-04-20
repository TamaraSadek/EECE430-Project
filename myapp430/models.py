from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Team DB( team name, members, team leader, description)
class Team(models.Model):
	team_id = models.IntegerField(primary_key=True)
	description = models.TextField()
	team_name= models.TextField()

	def __str__(self):
		return self.team_name

class Employee(models.Model):
	CATEGORY = (
			('Employee', 'Employee'),
			('Employer', 'Employer'),
			('Team Manager', 'Team Manager'),
			('Well-being Specialist', 'Well-being Specialist'),
			('HR Specialist','HR Specialist')
			) 
	employee_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="Name can only contain letters and spaces.")])
	phone = models.CharField(max_length=15, null=True)
	email = models.CharField(max_length=200)
	position = models.CharField(max_length=200, choices=CATEGORY)
	team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)  
	address = models.CharField(max_length=200, null=True)
	points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

	def clean(self):
		if self.phone and not self.phone.isdigit():
			raise ValidationError("Phone number can only contain digits.")
		
		if '@' not in self.email or '.' not in self.email:
			raise ValidationError("Invalid email.")
		
		if self.points < 0:
			raise ValidationError("Points can't be negative.")

	def __str__(self):
		return self.name
	@property
	def tasks(self):
		task_count = self.task_set.all().count()
		return str(task_count)
	

class Task(models.Model):

	STATUS = (
			('Complete', 'Complete'),
			('In Progress', 'In Progress'),
			) 
	task_id = models.AutoField(primary_key=True)
	employees = models.ManyToManyField(Employee, blank=True)
	deadline=  models.DateTimeField() #we will accept any date, even ones that passed, asuuming the client might want to add a completed task simply for book-keeping purposes
	points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	description = models.TextField()
	status = models.CharField(choices=STATUS, default='In Progress', max_length=11)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	credited = models.BooleanField(default=False)

	def __str__(self):
		employee_names = ', '.join(str(employee) for employee in self.employees.all())
		return f"{self.description} - Employees: {employee_names}"
	def clean(self):
		if self.points < 0:
			raise ValidationError("Points can't be negative.")

class Goals(models.Model):
	STATUS = (
		('Complete', 'Complete'),
		('In Progress', 'In Progress'),
		) 
	goal_id = models.AutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete= models.SET_NULL, null=True)
	deadline=  models.DateTimeField()
	description = models.TextField()
	status = models.CharField(choices=STATUS, default='In Progress', max_length=11)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.description
	def clean(self):
		if self.deadline <= timezone.now():
			raise ValidationError("Deadline must be in the future.")

class Mood(models.Model): #- Mood DB (mood, date, employee, team id)
	STATUS = (
		('Awful', 'Awful'),
		('Bad', 'Bad'),
        ('Neutral', 'Neutral'),
		('Good','Good'),
        ('Amazing', 'Amazing'),
		) 
	mood = models.CharField(max_length=20, choices=STATUS)
	employee = models.ForeignKey(Employee, on_delete= models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	team_id = models.IntegerField(null=True)

	def __str__(self):
		return self.mood

class Events(models.Model): #- Events DB (event id,event name, description, date, location)
	event_id = models.AutoField(primary_key=True)
	event_name = models.TextField()
	description = models.TextField()
	date = models.DateTimeField(null=True, blank=True)
	location=models.TextField()

	def __str__(self):
		return self.event_name
	def clean(self):
		if self.date < timezone.now():
			raise ValidationError("Date must be in the future.")
		
class Resource(models.Model):
	resource_id = models.AutoField(primary_key=True)
	resource_name = models.TextField()
	resource_description = models.TextField()
	link = models.URLField(blank=True, null=True)  # New field for links
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	last_modified = models.DateTimeField(auto_now=True)  # New field for last modification time

	def __str__(self):
		return self.resource_name


class EventRegistration(models.Model):
	event = models.ForeignKey(Events, on_delete=models.CASCADE)
	participant = models.ForeignKey(User, on_delete=models.CASCADE)
	registration_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ['event', 'participant'] #prevent users from signing up to the same event multiple times

	def __str__(self):
		return self.event_name

#- Rewards DB (reward tname, description, price(points), stock)
class Rewards(models.Model): 
	reward_name = models.TextField()
	description = models.TextField()
	stock = models.IntegerField(default=0)
	price = models.IntegerField(default=0)

	def __str__(self):
		return self.gift_name
	def clean(self):
		if self.stock < 0 or self.price < 0:
			raise ValidationError("Cannot be negative.")