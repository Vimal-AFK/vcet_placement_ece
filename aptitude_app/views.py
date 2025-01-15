from django.shortcuts import render

# Create your views here.
def index (request):
    return render(request,'index.html')

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
    return render(request, 'test.html', {"questions": questions_data})
