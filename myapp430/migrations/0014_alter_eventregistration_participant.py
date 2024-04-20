# Generated by Django 4.2.10 on 2024-04-16 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("myapp430", "0013_employee_user_alter_mood_mood"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventregistration",
            name="participant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
