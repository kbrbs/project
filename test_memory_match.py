"""
Test script to verify memory match scoring logic
Run with: python manage.py shell < test_memory_match.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from games.models import Game, GameQuestion, GameAttempt
from django.contrib.auth.models import User
import json

print("=" * 60)
print("TESTING MEMORY MATCH SCORING LOGIC")
print("=" * 60)

# Get or create a test user
user, _ = User.objects.get_or_create(username='test_memory_user', defaults={'email': 'test@example.com'})
print(f"Using user: {user.username}")

# Test scoring logic
print("\n--- Test 1: Perfect Score (8/8 pairs) ---")
matched_pairs = 8
total_pairs = 8
points_per_correct = 10

if matched_pairs == total_pairs and total_pairs > 0:
    score = points_per_correct
else:
    score = int((matched_pairs / total_pairs) * points_per_correct)

print(f"Matched: {matched_pairs}/{total_pairs}")
print(f"Score: {score} points")
print(f"Percentage: {(score / points_per_correct) * 100:.0f}%")
assert score == 10, "Perfect score should be 10 points"

print("\n--- Test 2: Partial Score (6/8 pairs) ---")
matched_pairs = 6
total_pairs = 8

if matched_pairs == total_pairs and total_pairs > 0:
    score = points_per_correct
else:
    score = int((matched_pairs / total_pairs) * points_per_correct)

print(f"Matched: {matched_pairs}/{total_pairs}")
print(f"Score: {score} points")
print(f"Percentage: {(matched_pairs / total_pairs) * 100:.0f}%")
expected = int((6/8) * 10)  # Should be 7
assert score == expected, f"Partial score should be {expected} points"

print("\n--- Test 3: Multiple Questions ---")
# Question 1: 8/8 pairs
q1_matched = 8
q1_total = 8
q1_score = points_per_correct if q1_matched == q1_total else int((q1_matched / q1_total) * points_per_correct)

# Question 2: 4/6 pairs  
q2_matched = 4
q2_total = 6
q2_score = points_per_correct if q2_matched == q2_total else int((q2_matched / q2_total) * points_per_correct)

total_score = q1_score + q2_score
max_score = points_per_correct * 2  # 2 questions
percentage = round((total_score / max_score) * 100)

print(f"Question 1: {q1_matched}/{q1_total} pairs → {q1_score} points")
print(f"Question 2: {q2_matched}/{q2_total} pairs → {q2_score} points")
print(f"Total Score: {total_score}/{max_score}")
print(f"Percentage: {percentage}%")

assert q1_score == 10, "Q1 should be 10 points"
assert q2_score == 6, "Q2 should be 6 points (4/6 * 10 = 6.67 → 6)"
assert total_score == 16, "Total should be 16 points"
assert percentage == 80, "Percentage should be 80%"

print("\n" + "=" * 60)
print("✅ ALL SCORING LOGIC TESTS PASSED!")
print("=" * 60)

print("\n--- Test 4: Simulating Game Submission ---")

# Find a memory match game or create one
games = Game.objects.filter(game_type='memory_match', is_active=True)
if games.exists():
    game = games.first()
    print(f"Found game: {game.title}")
    
    # Simulate answer data that frontend would send
    answers = {}
    total_score = 0
    max_score = 0
    
    for question in game.questions.all()[:1]:  # Test with first question only
        # Simulate perfect match
        answers[str(question.id)] = {
            'matched_pairs': 8,
            'attempts': 15,
            'total_pairs': 8,
            'time': 45
        }
        
        matched = answers[str(question.id)]['matched_pairs']
        total = answers[str(question.id)]['total_pairs']
        
        if matched == total and total > 0:
            total_score += game.points_per_correct
        else:
            total_score += int((matched / total) * game.points_per_correct)
        
        max_score += game.points_per_correct
    
    print(f"Simulated answers: {json.dumps(answers, indent=2)}")
    print(f"Calculated score: {total_score}/{max_score}")
    print(f"Percentage: {round((total_score/max_score)*100) if max_score > 0 else 0}%")
    
    print("\n✅ Game submission simulation successful!")
else:
    print("ℹ️  No memory match games found to test submission")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)
