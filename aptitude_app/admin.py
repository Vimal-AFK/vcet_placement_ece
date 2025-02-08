from django.contrib import admin
from .models import QuestionPaper, Question, Material, StudentResults 

from django.contrib import admin
admin.site.site_header = "ECE Placement Cell"
admin.site.site_title = "ECE Placement Cell Portal"
admin.site.index_title = "Welcome to the ECE Placement Cell Admin Panel"


# Inline for adding Questions to a QuestionPaper in one form
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0  # Shows one extra blank question form

# Admin configuration for QuestionPaper
@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = (
        'paper_code', 
        'paper_title', 
        'time_limit', 
        'total_marks', 
        'is_practice_paper', 
        'is_assessment_paper'
    )
    search_fields = ('paper_code', 'paper_title')
    list_filter = ('is_practice_paper', 'is_assessment_paper')
    inlines = [QuestionInline]
    ordering = ('paper_code',)
    fieldsets = (
        (None, {
            'fields': ('paper_code', 'paper_title', 'paper_description')
        }),
        ('Settings', {
            'fields': ('time_limit', 'no_of_qs', 'total_marks', 'is_practice_paper', 'is_assessment_paper')
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_paper', 
        'question_text', 
        'mark', 
        'correct_option'
    )
    search_fields = ('question_text',)
    list_filter = ('question_paper',)
    ordering = ('question_paper',)

# Admin configuration for Material uploads
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)
    
# Admin configuration for Student Results
@admin.register(StudentResults)
class StudentResultsAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'test_code', 
        'percentage', 
        'attended', 
        'status', 
        'date_of_exam', 
        'time'
    )
    search_fields = ('user__username', 'test_code')
    list_filter = ('test_code','status', 'attended', 'date_of_exam')
    ordering = ('-date_of_exam',)
    
    # Add date hierarchy for easier filtering by date
    date_hierarchy = 'date_of_exam'

    # Display percentage with proper formatting
    def percentage(self, obj):
        return f"{obj.percentage:.2f}%"
    percentage.short_description = "Percentage"
    
    # Customize the 'status' column for better readability
    def status(self, obj):
        return "Passed" if obj.status else "Failed"
    status.short_description = "Exam Status"



from django.contrib import admin
from .models import GlobalSettings

from django.contrib import admin
from .models import GlobalSettings

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('about_us', 'signup_option')

