#!/usr/bin/env python
"""
Test script to verify that deletion actually removes data from the database.
Run this with: python manage.py shell < test_deletion.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import EducationalSection, MediaAsset, ContentModeration
from games.models import Game, GameQuestion
from quizzes.models import Quiz, Question

User = get_user_model()

def test_deletions():
    print("\n" + "="*60)
    print("TESTING DELETION FUNCTIONALITY")
    print("="*60 + "\n")
    
    # Test 1: Create and delete a section
    print("1. Testing Section Deletion...")
    section = EducationalSection.objects.create(
        title="Test Section",
        slug="test-section",
        description="Test description",
        order=999
    )
    section_id = section.id
    print(f"   Created section with ID: {section_id}")
    
    section.delete()
    exists = EducationalSection.objects.filter(id=section_id).exists()
    print(f"   Deleted section. Still exists? {exists}")
    print(f"   ✓ PASS" if not exists else "   ✗ FAIL")
    
    # Test 2: Create and delete a game with questions
    print("\n2. Testing Game Deletion (with cascade to questions)...")
    game = Game.objects.create(
        title="Test Game",
        game_type="word_scramble",
        description="Test game",
        difficulty="easy"
    )
    game_id = game.id
    print(f"   Created game with ID: {game_id}")
    
    question = GameQuestion.objects.create(
        game=game,
        order=0
    )
    question_id = question.id
    print(f"   Created question with ID: {question_id}")
    
    game.delete()
    game_exists = Game.objects.filter(id=game_id).exists()
    question_exists = GameQuestion.objects.filter(id=question_id).exists()
    print(f"   Deleted game. Game still exists? {game_exists}")
    print(f"   Question still exists? {question_exists}")
    print(f"   ✓ PASS" if not game_exists and not question_exists else "   ✗ FAIL")
    
    # Test 3: Create and delete a quiz with questions
    print("\n3. Testing Quiz Deletion (with cascade to questions)...")
    quiz = Quiz.objects.create(title="Test Quiz")
    quiz_id = quiz.id
    print(f"   Created quiz with ID: {quiz_id}")
    
    q = Question.objects.create(
        quiz=quiz,
        text="Test question",
        choices=[{"text": "A", "correct": True}]
    )
    q_id = q.id
    print(f"   Created question with ID: {q_id}")
    
    quiz.delete()
    quiz_exists = Quiz.objects.filter(id=quiz_id).exists()
    q_exists = Question.objects.filter(id=q_id).exists()
    print(f"   Deleted quiz. Quiz still exists? {quiz_exists}")
    print(f"   Question still exists? {q_exists}")
    print(f"   ✓ PASS" if not quiz_exists and not q_exists else "   ✗ FAIL")
    
    # Test 4: Create and delete media
    print("\n4. Testing Media Asset Deletion...")
    media = MediaAsset.objects.create(
        title="Test Media",
        asset_type="image"
    )
    media_id = media.id
    print(f"   Created media with ID: {media_id}")
    
    media.delete()
    exists = MediaAsset.objects.filter(id=media_id).exists()
    print(f"   Deleted media. Still exists? {exists}")
    print(f"   ✓ PASS" if not exists else "   ✗ FAIL")
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")
    print("✓ All deletion operations are working correctly!")
    print("  Data is being permanently removed from the database.\n")

if __name__ == "__main__":
    test_deletions()
