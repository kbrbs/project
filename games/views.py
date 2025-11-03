from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from games.models import Game, GameQuestion, GameOption, GameAttempt
import json
import random
from django.db.models import Q


def game_list(request):
    """Public listing of available games."""
    games = Game.objects.filter(is_active=True).prefetch_related('questions')
    
    # Filter by type
    game_type = request.GET.get('type')
    if game_type:
        games = games.filter(game_type=game_type)
    
    # Search
    q = request.GET.get('q')
    if q:
        games = games.filter(Q(title__icontains=q) | Q(description__icontains=q))
    
    context = {
        'games': games,
        'game_types': Game.GAME_TYPE_CHOICES,
    }
    return render(request, 'games/game_list.html', context)


def game_detail(request, pk):
    """Game detail and play interface."""
    game = get_object_or_404(Game.objects.prefetch_related('questions__options'), pk=pk, is_active=True)
    questions = game.questions.all()
    
    # Prepare game data based on type
    game_data = {
        'id': game.id,
        'title': game.title,
        'type': game.game_type,
        'description': game.description,
        'time_limit': game.time_limit,
        'points_per_correct': game.points_per_correct,
        'questions': []
    }
    
    for q in questions:
        question_data = {
            'id': q.id,
            'text': q.question_text,
            'order': q.order,
        }
        
        if game.game_type == 'word_scramble':
            # Scramble the word on server side for consistency
            word = q.word.upper()
            scrambled = ''.join(random.sample(word, len(word)))
            question_data['scrambled'] = scrambled
            question_data['answer'] = word
            
        elif game.game_type == 'drag_drop':
            # Shuffle the sequence
            sequence = q.get_correct_sequence_list()
            shuffled = sequence.copy()
            random.shuffle(shuffled)
            question_data['items'] = shuffled
            question_data['correct_order'] = sequence
            
        elif game.game_type in ['image_identification', 'multiple_choice_image']:
            # Get options
            options = list(q.options.all())
            random.shuffle(options)
            question_data['options'] = [
                {
                    'id': opt.id,
                    'text': opt.option_text,
                    'image': opt.option_image.url if opt.option_image else None,
                    'is_correct': opt.is_correct
                }
                for opt in options
            ]
            
        elif game.game_type == 'memory_match':
            # Get pairs and create card list
            pairs = q.get_memory_pairs_dict()
            cards = []
            for key, value in pairs.items():
                cards.append({'text': key, 'pair_id': key})
                cards.append({'text': value, 'pair_id': key})
            random.shuffle(cards)
            question_data['cards'] = cards
        
        question_data['explanation'] = q.explanation
        game_data['questions'].append(question_data)
    
    context = {
        'game': game,
        'game_data_json': json.dumps(game_data),
    }
    return render(request, f'games/{game.game_type}_game.html', context)


@login_required
@require_POST
def submit_game(request, pk):
    """Submit game answers and calculate score."""
    game = get_object_or_404(Game, pk=pk)
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        time_taken = data.get('time_taken', None)
        
        score = 0
        max_score = 0
        
        for question in game.questions.all():
            max_score += game.points_per_correct
            user_answer = answers.get(str(question.id))
            
            if game.game_type == 'word_scramble':
                if user_answer and user_answer.upper() == question.word.upper():
                    score += game.points_per_correct
                    
            elif game.game_type == 'drag_drop':
                correct_sequence = question.get_correct_sequence_list()
                if user_answer == correct_sequence:
                    score += game.points_per_correct
                    
            elif game.game_type in ['image_identification', 'multiple_choice_image']:
                # user_answer is option_id
                try:
                    option = question.options.get(id=int(user_answer))
                    if option.is_correct:
                        score += game.points_per_correct
                except:
                    pass
                    
            elif game.game_type == 'memory_match':
                # For memory match, count correct pairs
                # user_answer should be a dict of matched pairs
                pairs = question.get_memory_pairs_dict()
                if isinstance(user_answer, dict):
                    # Check if pairs match correctly
                    correct_pairs = 0
                    for key, value in user_answer.items():
                        if key in pairs and pairs[key] == value:
                            correct_pairs += 1
                    # Award partial credit
                    if len(pairs) > 0:
                        score += int((correct_pairs / len(pairs)) * game.points_per_correct)
        
        # Save attempt
        attempt = GameAttempt.objects.create(
            user=request.user,
            game=game,
            score=score,
            max_score=max_score,
            time_taken=time_taken,
            answers=json.dumps(answers),
            completed=True
        )
        
        return JsonResponse({
            'success': True,
            'score': score,
            'max_score': max_score,
            'percentage': attempt.get_percentage(),
            'attempt_id': attempt.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def my_attempts(request):
    """View user's game attempt history."""
    attempts = GameAttempt.objects.filter(user=request.user).select_related('game').order_by('-created_at')
    
    context = {
        'attempts': attempts,
    }
    return render(request, 'games/my_attempts.html', context)
