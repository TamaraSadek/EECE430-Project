# Generated by Django 3.2.24 on 2024-04-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp430', '0009_auto_20240403_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='employees',
            field=models.ManyToManyField(blank=True, null=True, to='myapp430.Employee'),
        ),
    ]
