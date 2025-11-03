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
            # New fill-in-the-blanks format
            if q.sentence_template:
                # Parse sentence template and create blanks
                sentence = q.sentence_template
                correct_answers = q.get_correct_answers_list()
                extra_choices = q.get_extra_choices_list()
                
                # Replace * and _ with numbered placeholders
                blank_count = 0
                sentence_parts = []
                current_part = ""
                
                for char in sentence:
                    if char in ['*', '_']:
                        if current_part:
                            sentence_parts.append({'type': 'text', 'content': current_part})
                            current_part = ""
                        sentence_parts.append({'type': 'blank', 'index': blank_count})
                        blank_count += 1
                    else:
                        current_part += char
                
                if current_part:
                    sentence_parts.append({'type': 'text', 'content': current_part})
                
                # Combine all choices and shuffle
                all_choices = correct_answers + extra_choices
                random.shuffle(all_choices)
                
                question_data['sentence_parts'] = sentence_parts
                question_data['choices'] = all_choices
                question_data['correct_answers'] = correct_answers
                question_data['blank_count'] = blank_count
            else:
                # Legacy sorting format (backward compatibility)
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
                # Check if using new fill-in-the-blanks format
                if question.sentence_template:
                    # user_answer is a dict/list of blank_index: answer
                    correct_answers = question.get_correct_answers_list()
                    
                    if isinstance(user_answer, dict):
                        # Check each blank
                        all_correct = True
                        for i, correct in enumerate(correct_answers):
                            user_ans = user_answer.get(str(i), '').strip()
                            if user_ans.lower() != correct.lower():
                                all_correct = False
                                break
                        if all_correct:
                            score += game.points_per_correct
                    elif isinstance(user_answer, list):
                        # Alternative: list format [answer1, answer2, ...]
                        if len(user_answer) == len(correct_answers):
                            all_correct = all(
                                user_ans.strip().lower() == correct.lower()
                                for user_ans, correct in zip(user_answer, correct_answers)
                            )
                            if all_correct:
                                score += game.points_per_correct
                else:
                    # Legacy sorting format
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
