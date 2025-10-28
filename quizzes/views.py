from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Quiz


def quiz_list(request):
    qs = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': qs})


def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})


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
