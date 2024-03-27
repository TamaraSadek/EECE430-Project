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
	team_id = models.IntegerField(null=True)
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
			(1, 'Complete'),
			(0, 'In Progress'),
			) 
	task_id = models.AutoField(primary_key=True)
	employee = models.ForeignKey(Employee, on_delete= models.SET_NULL, null=True)
	deadline=  models.DateTimeField()
	points = models.IntegerField(default=0)
	description = models.TextField()
	status = models.IntegerField(choices=STATUS, default=0)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.description
