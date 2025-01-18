from django.db import models


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
        return f"{self.department} - Batch {self.batch_year} ({self.year}) - {self.total_strength}"


class Student(models.Model):
    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=20, unique=True, db_index=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
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
        self.average_percentage = self.calculate_average_percentage()
        if not self.password:
            self.password = self.date_of_birth.strftime('%Y%m%d')
        super().save(*args, **kwargs)

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
