from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    university_number = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    batch_year = models.IntegerField(default=2026, null=True)
    section = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1), null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    GENDER_CHOICE = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]
    gender = models.CharField(max_length=6, default='Male', choices=GENDER_CHOICE, null=True)
    average_percentage = models.FloatField(default=0, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class StudentResults(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, related_name='auth_studentresults')
    test_code = models.CharField(max_length=20, null=True)
    test_title = models.CharField(max_length=255, null=True)
    date_of_exam = models.DateField(null=True)
    time = models.TimeField(null=True)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True , blank=True)
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Malpractice', 'Malpractice'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed', null=True)
    attended = models.BooleanField(default=False, null=True)