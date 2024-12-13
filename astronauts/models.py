from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom user model
class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)  # Admin approval field

    def __str__(self):
        return self.username


# Updated Astronaut model to reference the custom user
class Astronaut(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='astronauts',
        null=True,  # Allow no user
        blank=True  # Optional field
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    joined_date = models.DateField()
    missions = models.ManyToManyField('Mission', related_name='astronauts', blank=True)

    def __str__(self):
        return self.name


# Updated Mission model to reference CustomUser
class Mission(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    objectives = models.TextField()  # Correct field for mission objectives
    crew_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='missions')  # Reference CustomUser
    status = models.CharField(
        max_length=20,
        choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')],
        default='Planned'
    )

    def __str__(self):
        return self.name


# Updated Task model to reference CustomUser
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')  # Reference CustomUser
    due_date = models.DateField()
    priority = models.CharField(
        max_length=20,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Medium'
    )
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='Pending'
    )

    def __str__(self):
        return self.title


# Updated Training model to reference CustomUser
class Training(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    materials = models.FileField(upload_to='training_materials/', blank=True, null=True)
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainings_provided')  # Reference CustomUser
    completed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='completed_trainings', blank=True)  # Reference CustomUser

    def __str__(self):
        return self.title


class BMIRecord(models.Model):
    astronaut = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField(editable=False, blank=True, null=True)  # Add this field
    oxygen_level = models.FloatField(default=95.0)
    glycerol_level = models.FloatField(default=100.0)
    calorie_intake = models.FloatField()
    daily_stool = models.FloatField()
    water_intake = models.FloatField(default=2000.0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically calculate and save BMI
        if self.height > 0:
            self.bmi = self.weight / (self.height ** 2)
        else:
            self.bmi = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"BMI: {self.bmi if self.bmi else 'N/A'}, Date: {self.recorded_at}"
