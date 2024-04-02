from django.db import models

class Employee(models.Model):
	CATEGORY = (
			('Employee', 'Employee'),
			('Employer', 'Employer'),
			('Team Manager', 'Team Manager'),
			('Well-being Specialist', 'Well-being Specialist'),
			('HR Specialist','HR Specialist')
			) 
	employee_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=15, null=True)
	email = models.CharField(max_length=200)
	position = models.CharField(max_length=200,choices=CATEGORY)
	team_id = models.IntegerField(null=True) # should this be from Team DB?? 
	address=models.CharField(max_length=200, null=True)
	points=models.IntegerField(default=0)

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
	employee = models.ForeignKey(Employee, on_delete= models.SET_NULL, null=True)
	deadline=  models.DateTimeField()
	points = models.IntegerField(default=0)
	description = models.TextField()
	status = models.CharField(choices=STATUS, default='In Progress', max_length=11)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	credited = models.BooleanField(default=False)

	def __str__(self):
		return self.description


class Goals(models.Model):
	STATUS = (
		('Complete', 'Complete'),
		('In Progress', 'In Progress'),
		) 
	goal_id = models.AutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete= models.SET_NULL, null=True)
	deadline=  models.DateTimeField()
	points = models.IntegerField(default=0)
	description = models.TextField()
	status = models.CharField(choices=STATUS, default='In Progress', max_length=11)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


def __str__(self):
	return self.description

class Mood(models.Model): #- Mood DB (mood, date, employee, team id)
	STATUS = (
		('Complete', 'Complete'),
		('In Progress', 'In Progress'),
		) 
	mood=models.TextField()
	employee = models.ForeignKey(Employee, on_delete= models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	team_id = models.IntegerField(null=True)

def __str__(self):
	return self.mood

class Events(models.Model): #- Events DB (event id,event name, description, date, location)
	event_name = models.TextField()
	event_id = models.AutoField(primary_key=True)
	description = models.TextField()
	date = models.DateTimeField(null=True, blank=True)
	location=models.TextField()

class EventRegistration(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    participant = models.ForeignKey(Employee, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'participant'] #prevent users from signing up to the same event multiple times

def __str__(self):
	return self.event_name

#- Gifts DB (giftname, description, price(points), stock)
class Gifts(models.Model): 
	gift_name=models.TextField()
	description = models.TextField()
	stock=models.IntegerField(default=0)
	price=models.IntegerField(default=0)
def __str__(self):
	return self.gift_name
	
# Team DB( team name, members, team leader, description)
class Team(models.Model):
	team_id = models.AutoField(primary_key=True)
	members = models.ManyToManyField(Employee)
	description = models.TextField()
	team_name= models.TextField()

def __str__(self):
	return self.team_name