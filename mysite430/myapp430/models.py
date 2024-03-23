from django.db import models

# Create your models here.
class Employee(models.Model):
	CATEGORY = (
			('Employee', 'Employee'),
			('Employer', 'Employer'),
			('Team Manager', 'Team Manager'),
			('Well-being Specialist', 'Well-being Specialist'),
			('HR Specialist','HR Specialist')
			) 
	employee_id = models.IntegerField(default=0, max_length=200)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	position = models.CharField(max_length=200, null=True,choices=CATEGORY)
	team_id = models.IntegerField(max_length=200, null=True)
	address=models.CharField(max_length=200, null=True)
	points=models.IntegerField(max_length=200, default=0)

	def __str__(self):
		return self.name
	


class Task(models.Model):

	STATUS = (
			(1, 'Complete'),
			(0, 'In Progress'),
			) 
	task_id = models.IntegerField(max_length=200, null=True)
	employee_id = models.IntegerField(default=0, max_length=200)
	deadline=  models.DateTimeField(auto_now_add=True, null=True, blank=True)
	points = models.IntegerField(max_length=200, null=True)
	description = models.TextField()
	status = models.IntegerField(choices=STATUS)
	

	def __str__(self):
		return self.description
