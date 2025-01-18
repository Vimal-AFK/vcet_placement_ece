from django.contrib import admin
from .models import Batch, Student, Result


# Inline for Students within a Batch
class StudentInline(admin.TabularInline):
    model = Student
    extra = 0  # Do not show extra empty rows
    fields = ('name', 'roll_number', 'section', 'email', 'average_percentage')  # Relevant fields to display
    readonly_fields = ('name', 'roll_number', 'section', 'email', 'average_percentage')  # Make fields non-editable
    show_change_link = True  # Enable link to StudentAdmin details


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_year', 'year','total_strength' )  # Show basic batch info
    search_fields = ('batch_year', 'year')
    ordering = ('batch_year', 'year')
    list_filter = ('year', 'batch_year')
    inlines = [StudentInline]  # Show students in the batch
    fields = ('batch_year', 'year','total_strength' )  # Add year field


# Inline for Results within a Student
class ResultInline(admin.TabularInline):
    model = Result
    extra = 0  # Allows one extra inline entry for adding results quickly

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'batch', 'section', 'gender', 'email')
    search_fields = ('name', 'roll_number', 'email')
    list_filter = ('batch', 'section', 'gender')
    ordering = ('batch', 'roll_number')
    inlines = [ResultInline]  # Add Result management directly in Student admin view
    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'date_of_birth', 'gender', 'email', 'phone_number', 'password')  # Add password field
        }),
        ('Academic Info', {
            'fields': ('batch', 'roll_number', 'section', 'average_percentage')
        }),
    )
    exclude = ()  # Remove exclusion of password field


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test_code', 'date_of_exam', 'total_marks_scored', 'percentage', 'status', 'attended')
    search_fields = ('student__name', 'test_code')
    list_filter = ('status', 'test_code', 'date_of_exam', 'student__batch', 'student__section', 'student__gender')  # Add filters
    ordering = ('-date_of_exam',)
    autocomplete_fields = ('student',)
    readonly_fields = ('student', 'test_code', 'date_of_exam', 'total_marks_scored', 'percentage', 'status')  # Make fields non-editable

admin.site.site_header = "VCET Placement Cell of ECE"
admin.site.site_title = "VCET Placement Admin"
admin.site.index_title = "Welcome to Admin Panel"
