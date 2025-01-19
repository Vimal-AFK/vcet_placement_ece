from django.db import models
from django.urls import reverse


class Batch(models.Model):
    class DepartmentChoices(models.TextChoices):
        ECE = 'ECE', 'Electronics and Communication Engineering'
        CSE = 'CSE', 'Computer Science Engineering'
        MECH = 'MECH', 'Mechanical Engineering'
        EEE = 'EEE', 'Electrical and Electronics Engineering'
        CIVIL = 'CIVIL', 'Civil Engineering'
        IT = 'IT', 'Information Technology'

    class YearChoices(models.IntegerChoices):
        FIRST_YEAR = 1, '1st Year'
        SECOND_YEAR = 2, '2nd Year'
        THIRD_YEAR = 3, '3rd Year'
        FOURTH_YEAR = 4, '4th Year'

    department = models.CharField(
        max_length=20,
        choices=DepartmentChoices.choices,
        default=DepartmentChoices.ECE,
    )
    batch_year = models.PositiveIntegerField()
    total_strength = models.PositiveIntegerField()
    year = models.PositiveIntegerField(choices=YearChoices.choices, default=YearChoices.FIRST_YEAR)  # Add year field with choices

    class Meta:
        ordering = ['batch_year']
        constraints = [
            models.UniqueConstraint(fields=['batch_year', 'department'], name='unique_batch_year_department')
        ]
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"{self.department} - Batch {self.batch_year} ({self.year}Year) - {self.total_strength}"


class Student(models.Model):
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=20, unique=True, db_index=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    password = models.CharField(max_length=128, editable=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    average_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['batch', 'roll_number'], name='unique_roll_in_batch'),
        ]

    def calculate_average_percentage(self):
        results = self.results.filter(attended=True)
        if results.exists():
            total_percentage = sum(result.percentage for result in results)
            return total_percentage / results.count()
        return 0

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance already exists
            self.average_percentage = self.calculate_average_percentage()
        if not self.password:
            self.password = self.date_of_birth.strftime('%Y%m%d')
        super().save(*args, **kwargs)
        if not self.pk:  # Calculate average percentage after saving the new instance
            self.average_percentage = self.calculate_average_percentage()
            super().save(update_fields=['average_percentage'])

    def __str__(self):
        return f"{self.name} ({self.roll_number}) - Batch {self.batch.batch_year}"


class Result(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('malpracticed', 'Malpracticed'),
        ('reappeared', 'Reappeared'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    test_code = models.CharField(max_length=4, db_index=True)
    date_of_exam = models.DateField()
    total_marks_scored = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    attended = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_of_exam']
        constraints = [
            models.UniqueConstraint(fields=['student', 'test_code'], name='unique_test_per_student'),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.student.average_percentage = self.student.calculate_average_percentage()
        self.student.save(update_fields=['average_percentage'])

    def __str__(self):
        return f"Result: {self.student.name} - {self.test_code} ({self.percentage}%)"
    
from django.db import models
import uuid


class QuestionPaper(models.Model):
    # Core fields
    paper_code = models.CharField(
        max_length=4, unique=True, editable=False, default=uuid.uuid4().hex[:4]
    )
    paper_title = models.CharField(max_length=255)
    paper_description = models.TextField(blank=True, null=True)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    total_marks = models.PositiveIntegerField(default=0)  # Calculated dynamically
    is_practice_paper = models.BooleanField(default=False)
    is_assessment_paper = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.paper_title} ({self.paper_code})"

    def calculate_total_marks(self):
        self.total_marks = sum(q.mark for q in self.questions.all())
        self.save()

    def get_absolute_url(self):
        return reverse('question_paper_preview', args=[str(self.id)])

    class Meta:
        verbose_name = "Question Paper"
        verbose_name_plural = "Question Papers"


class Question(models.Model):
    # Link to QuestionPaper
    question_paper = models.ForeignKey(
        QuestionPaper, related_name='questions', on_delete=models.CASCADE, default=1
    )
    question_text = models.TextField(blank=True, null=True)
    question_image = models.ImageField(upload_to='questions/', blank=True, null=True)
    mark = models.PositiveIntegerField(default=1)

    # MCQ fields
    option_A = models.CharField(max_length=255, blank=True, null=True)
    option_B = models.CharField(max_length=255, blank=True, null=True)
    option_C = models.CharField(max_length=255, blank=True, null=True)
    option_D = models.CharField(max_length=255, blank=True, null=True)
    CORRECT_OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    correct_option = models.CharField(
        max_length=1, choices=CORRECT_OPTION_CHOICES, blank=True, null=True, help_text="Key of the correct option for MCQs."
    )

    def __str__(self):
        return f"Question {self.id} for {self.question_paper.paper_code}"

    def clean(self):
        # Ensure MCQ fields are filled
        if not self.option_A or not self.option_B or not self.option_C or not self.option_D or not self.correct_option:
            raise ValueError("MCQs must have 4 options and a correct option.")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


