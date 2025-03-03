from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime


class QuestionPaper(models.Model):
    paper_code = models.CharField(max_length=10, unique=True)
    paper_title = models.CharField(max_length=255)
    paper_description = models.TextField(blank=True, null=True)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    no_of_qs = models.PositiveIntegerField(blank=True, null=True)
    total_marks = models.PositiveIntegerField(blank=True, null=True)
    is_practice_paper = models.BooleanField(default=True)
    is_assessment_paper = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.paper_title} ({self.paper_code})"

    def get_absolute_url(self):
        return reverse('question_paper_preview', args=[self.pk])

    class Meta:
        verbose_name = "Question Paper"
        verbose_name_plural = "Question Papers"



class Question(models.Model):
    question_paper = models.ForeignKey(
        QuestionPaper, related_name='questions', on_delete=models.CASCADE
    )
    question_text = models.TextField()
    mark = models.PositiveIntegerField(default=1)


    option_A = models.TextField()
    option_B = models.TextField()
    option_C = models.TextField()
    option_D = models.TextField()

    CORRECT_OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    correct_option = models.CharField(
        default='A',
        max_length=1,
        choices=CORRECT_OPTION_CHOICES,
        help_text="Key of the correct option for MCQs."
    )

    def __str__(self):
        return f"Question {self.pk} ({self.question_paper.paper_code})"

    def clean(self):
        super().clean()
        if not all([self.option_A, self.option_B, self.option_C, self.option_D, self.correct_option]):
            raise ValueError("MCQs must have all four options and a correct option selected.")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Material(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('material_detail', args=[self.pk])

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"


class StudentResults(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Malpractice', 'Malpractice'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='results')
    test_title = models.CharField(max_length=255, default='')
    test_code = models.CharField(max_length=10, default='')  
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    attended = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')
    date_of_exam = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Result for {self.user} - {self.test_code}"

    class Meta:
        verbose_name = "Student Result"
        verbose_name_plural = "Student Results"

from django.db import models

class GlobalSettings(models.Model):
    signup_option = models.BooleanField(default=False)  
    about_us = models.TextField(max_length=10000, default="Velammal")  
    notice_board = models.TextField(max_length=10000, default="Evaluate and sharpen your logical, numerical, and verbal reasoning abilities.")  
    
    def __str__(self):
        return "Global Settings"
    
class placement_stories(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    package = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='placement_stories/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Placement Story"
        verbose_name_plural = "Placement Stories"
