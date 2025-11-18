from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz
from core.utils import log_activity
from core.access_control import limit_public_access, get_public_access_context, PUBLIC_QUIZZES_LIMIT


def quiz_list(request):
    """Quiz list - fully public access to all quizzes."""
    qs = Quiz.objects.all()
    
    # Get total count
    total_quizzes = qs.count()
    
    context = {
        'quizzes': qs,
        'total_quizzes': total_quizzes,
    }
    context.update(get_public_access_context(request.user))
    return render(request, 'quizzes/quiz_list.html', context)


def quiz_detail(request, pk):
    """Quiz detail - public can take quizzes."""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    # Log quiz started (only for authenticated users)
    if request.user.is_authenticated:
        log_activity(
            user=request.user,
            category='quiz',
            action='quiz_started',
            description=f'Started quiz: {quiz.title}',
            request=request,
            quiz_id=quiz.id
        )
    
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})


def quiz_api_detail(request, pk):
    """API endpoint to get quiz data - public can access."""
    quiz = get_object_or_404(Quiz, pk=pk)
    data = {
        'id': quiz.id,
        'title': quiz.title,
        'questions': [
            {'id': q.id, 'text': q.text, 'choices': q.get_choices_json()}
            for q in quiz.questions.all()
        ]
    }
    return JsonResponse(data)


def quiz_submit(request, pk):
    """Submit quiz answers and return results with correct answers - public can submit."""
    import json
    from django.views.decorators.http import require_POST
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    quiz = get_object_or_404(Quiz, pk=pk)
    
    try:
        answers = json.loads(request.body)  # {'q_id': choice_id, ...}
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    results = []
    total_questions = 0
    correct_count = 0
    
    for question in quiz.questions.all():
        total_questions += 1
        user_answer = answers.get(str(question.id))
        
        # Get choices in JSON format
        choices = question.get_choices_json()
        
        # Find correct choice and user's choice
        correct_choice = None
        user_choice_text = None
        
        for choice in choices:
            if choice.get('correct'):
                correct_choice = choice
            if user_answer and str(choice.get('id')) == str(user_answer):
                user_choice_text = choice.get('text')
        
        is_correct = False
        if correct_choice and user_answer:
            is_correct = str(correct_choice.get('id')) == str(user_answer)
        
        if is_correct:
            correct_count += 1
        
        results.append({
            'question_id': question.id,
            'question_text': question.text,
            'user_answer': user_choice_text,
            'correct_answer': correct_choice.get('text') if correct_choice else None,
            'is_correct': is_correct,
            'answered': user_answer is not None
        })
    
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Log quiz completion (only for authenticated users)
    if request.user.is_authenticated:
        action = 'quiz_passed' if score_percentage >= 60 else 'quiz_failed'
        log_activity(
            user=request.user,
            category='quiz',
            action=action,
            description=f'Completed quiz: {quiz.title} - Score: {score_percentage:.1f}%',
            request=request,
            quiz_id=quiz.id,
            metadata={
                'score_percentage': score_percentage,
                'correct_count': correct_count,
                'total_questions': total_questions
            }
        )
    
    return JsonResponse({
        'total_questions': total_questions,
        'correct_count': correct_count,
        'score_percentage': round(score_percentage, 1),
        'results': results
    })
