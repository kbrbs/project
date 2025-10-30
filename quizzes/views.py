from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz


@login_required
def quiz_list(request):
    qs = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': qs})


@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})


@login_required
def quiz_api_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    data = {
        'id': quiz.id,
        'title': quiz.title,
        'questions': [
            {'id': q.id, 'text': q.text, 'choices': q.choices}
            for q in quiz.questions.all()
        ]
    }
    return JsonResponse(data)


@login_required
def quiz_submit(request, pk):
    """Submit quiz answers and return results with correct answers"""
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
        
        # Find correct choice
        correct_choice = None
        user_choice_text = None
        
        for choice in question.choices:
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
    
    return JsonResponse({
        'total_questions': total_questions,
        'correct_count': correct_count,
        'score_percentage': round(score_percentage, 1),
        'results': results
    })
