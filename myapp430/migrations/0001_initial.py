# Generated by Django 3.2.24 on 2024-03-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('email', models.CharField(max_length=200)),
                ('position', models.CharField(choices=[('Employee', 'Employee'), ('Employer', 'Employer'), ('Team Manager', 'Team Manager'), ('Well-being Specialist', 'Well-being Specialist'), ('HR Specialist', 'HR Specialist')], max_length=200)),
                ('team_id', models.IntegerField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('points', models.IntegerField(default=0, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(max_length=200)),
                ('employee_name', models.CharField(max_length=200)),
                ('deadline', models.DateTimeField()),
                ('points', models.IntegerField(default=0, max_length=200)),
                ('description', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'Complete'), (0, 'In Progress')], default=0)),
            ],
        ),
    ]
