from django.shortcuts import render, get_object_or_404
from .models import Student, QuestionPaper

# Create your views here.
def index (request):
    return render(request,'index.html')

def login(request):
    return render(request,'index_files/login.html')

def profile(request):
    student = Student.objects.get(id=request.user.id)
    return render(request, 'index_files/profile.html', {'student': student})

def test(request):
    questions_data = [
        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Rome"],
        },
        {
            "question": "What is 5 + 3?",
            "options": ["5", "8", "10", "15"],
        },
        {
            "question": "Which programming language is used for web development?",
            "options": ["Python", "JavaScript", "C++", "Java"],
        },
        {
            "question": "Which programming language is used for web development?",
            "options": ["Python", "JavaScript", "C++", "Java"],
        },
        {
            "question": "Which programming language is used for web development? sssssssssssssssssssssssssssssssssssssssssssssssssssgydgygdygdgydgdgygdigdihgdiuhdiuhuih",
            "options": ["Python", "JavaScript", "C++", "Java"],
        },
    ]
    return render(request, 'test_activity/test.html', {"questions": questions_data})

def question_paper_preview(request, id):
    question_paper = get_object_or_404(QuestionPaper, id=id)
    return render(request, 'question_paper_preview.html', {'question_paper': question_paper})
