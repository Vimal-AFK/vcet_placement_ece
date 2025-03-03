from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import PaperCodeForm, UserForm
from .models import QuestionPaper, Material, StudentResults, GlobalSettings , placement_stories
from authentication.models import User
from django.shortcuts import render

def index(request):
    settings, _ = GlobalSettings.objects.get_or_create(id=1)
    user_data = None

    if request.method == 'GET' and 'paper_code' in request.GET:
        form = PaperCodeForm(request.GET)
        if form.is_valid():
            paper_code = form.cleaned_data['paper_code']
            if QuestionPaper.objects.filter(paper_code=paper_code).exists():
                messages.success(request, 'Paper code is valid!')
                request.session['paper_code'] = paper_code
                return redirect('notice', paper_code=paper_code)
            else:
                messages.error(request, 'Invalid paper code!')
        else:
            messages.error(request, 'Invalid input!')

    if request.user.is_authenticated:
        user_data = User.objects.get(id=request.user.id)

    
        student_results = StudentResults.objects.filter(user=request.user)
        if student_results.exists():  
            user_data.average_percentage = sum(result.percentage for result in student_results) / student_results.count()
            user_data.save()
        else:   
            user_data.average_percentage = 0  
            user_data.save()

    stories = placement_stories.objects.all()

    context = {
        'paper_form': PaperCodeForm(),
        'materials': Material.objects.all(),
        'practice_papers': QuestionPaper.objects.filter(is_practice_paper=True),
        'student': request.user if request.user.is_authenticated else None,
        'results': StudentResults.objects.filter(user=request.user) if request.user.is_authenticated else None,
        'about_us_text': settings.about_us,
        'signup_enabled': settings.signup_option,
        'notice_board_text': settings.notice_board,
        'user_data': user_data,
        'placementStories' : placement_stories.objects.all(),
    }
    return render(request, 'index.html', context)

def signup(request):
    """
    Handles user signup.
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'index_files/signup.html', {'form': form})

def notice(request, paper_code):
    """
    Displays the test notice page and checks if the user is eligible to take the test.
    """
    paper = get_object_or_404(QuestionPaper, paper_code=paper_code)

    if not request.user.is_authenticated:
        messages.error(request, 'You need to log in to access the test.')
        return redirect('login')

    if StudentResults.objects.filter(user=request.user, test_code=paper_code, attended=True).exists():
        messages.warning(request, 'You have already attended this test.')
        return redirect('/#assessments')

    return render(request, 'test_activity/notice.html', {'paper': paper})

from django.shortcuts import render, get_object_or_404
from .models import StudentResults, QuestionPaper  # Assuming you have a QuestionPaper model

def test(request, paper_code):
    """
    Renders the test page with questions and checks if the user has already attended.
    """
    paper = get_object_or_404(QuestionPaper, paper_code=paper_code)
    
    # Check if the user has already attended the test
    attend = StudentResults.objects.filter(user=request.user, test_code=paper_code).exists()

    
    context = {
        'attend': attend,
        'paper': paper,
        'questions': paper.questions.all().order_by("?"),  # Assuming questions are related to QuestionPaper
    }
    print(attend)
    return render(request, 'test_activity/test.html', context)

def result(request, paper_code):
    """
    Handles test submission, calculates results, and saves them.
    """
    paper = get_object_or_404(QuestionPaper, paper_code=paper_code)

    if request.method == 'POST':
        score = sum(
            question.mark
            for question in paper.questions.all()
            if request.POST.get(f'question_{question.id}') == question.correct_option
        )
        time_taken = int(request.POST.get('time_taken', 0))
        total_marks = paper.total_marks or 0
        percentage = (score / total_marks) * 100 if total_marks > 0 else 0
        malpractice = request.POST.get('malpractice', 'false') == 'true'

        StudentResults.objects.update_or_create(
            user=request.user,
            test_code=paper_code,
            defaults={
                'test_title': paper.paper_title,
                'percentage': percentage,
                'attended': True,
                'status': 'Malpractice' if malpractice else 'Completed',
                'date_of_exam': timezone.now().date(),
                'time': timezone.now().time(),
            }
        )

        context = {
            'paper': paper,
            'score': score,
            'total_marks': total_marks,
            'percentage': percentage,
            'time_taken': time_taken,
            'malpractice': malpractice,
            'redirect_timeout': 7,
        }
        return render(request, 'test_activity/result.html', context)

    messages.error(request, 'Invalid request.')
    return redirect('index')

