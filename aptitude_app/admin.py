from django.contrib import admin
from django.http import HttpResponse
from django.db.models import QuerySet
import pandas as pd
from .models import QuestionPaper, Question, Material, StudentResults, GlobalSettings , placement_stories



admin.site.site_header = "ECE Placement Cell"
admin.site.site_title = "ECE Placement Cell Portal"
admin.site.index_title = "Welcome to the ECE Placement Cell Admin Panel"



class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0  


@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = (
        'paper_code',
        'paper_title',
        'time_limit',
        'no_of_qs',
        'total_marks',
    )
    search_fields = ('paper_code', 'paper_title')
    list_filter = ('paper_code','paper_title')
    inlines = [QuestionInline]
    ordering = ('paper_code',)
    fieldsets = (
        (None, {
            'fields': ('paper_code', 'paper_title', 'paper_description')
        }),
        ('Settings', {
            'fields': ('time_limit', 'no_of_qs', 'total_marks')
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_paper', 'serial_number','question_text', 'mark', 'get_correct_answer')
    search_fields = ('question_text',)
    list_filter = ('question_paper', 'question_paper__paper_code')  
    ordering = ('question_paper',)

    def serial_number(self, obj):
        return list(self.model.objects.all()).index(obj) + 1
    
    serial_number.short_description = 'S.No'

    def get_correct_answer(self, obj):
        correct_option_mapping = {
            'A': obj.option_A,
            'B': obj.option_B,
            'C': obj.option_C,
            'D': obj.option_D,
        }
        return correct_option_mapping.get(obj.correct_option, "N/A")
    
    get_correct_answer.short_description = 'Correct Answer'



@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('file','title', 'uploaded_at')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)


@admin.register(StudentResults)
class StudentResultsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'test_code',
        'percentage_display',
        'attended_display',
        'status_display',
        'date_of_exam',
        'time',
    )
    search_fields = ('user__username', 'test_code')
    list_filter = ('test_code', 'status', 'attended', 'date_of_exam')
    ordering = ('-date_of_exam',)
    actions = ['export_as_excel']
    date_hierarchy = 'date_of_exam'

    def percentage_display(self, obj) -> str:
        """Format percentage for display."""
        return f"{obj.percentage:.2f}%"
    percentage_display.short_description = "Percentage"

    # Custom method to display attendance status
    def attended_display(self, obj) -> str:
        """Format attendance status for display."""
        return "Yes" if obj.attended else "No"
    attended_display.short_description = "Attended"

    # Custom method to display exam status
    def status_display(self, obj) -> str:
        """Format exam status for display."""
        return "Passed" if obj.status else "Failed"
    status_display.short_description = "Exam Status"

    # Custom action to export selected records as Excel
    def export_as_excel(self, request, queryset: QuerySet) -> HttpResponse:
        """Export selected StudentResults records as an Excel file."""
        # Create a DataFrame from the queryset
        data = [
            {
                "University Number": result.user.university_number,
                "Roll Number" : result.user.roll_number,
                "Name": result.user.name,
                "User": result.user.username,
                "Test Code": result.test_code,
                "Percentage": f"{result.percentage:.2f}%",
                "Status": result.status,
                "Date of Exam": result.date_of_exam.strftime('%Y-%m-%d'),
                "Time": result.time.strftime('%H:%M:%S'),
            }
            for result in queryset
        ]

        df = pd.DataFrame(data)

        # Create an HTTP response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=student_results.xlsx'

        # Write the DataFrame to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Student Results')

        return response

    export_as_excel.short_description = "Export selected results as Excel"


# Admin configuration for GlobalSettings
@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('about_us', 'signup_option')
    list_editable = ('signup_option',)  # Allow editing directly from the list view


admin.site.register(placement_stories)